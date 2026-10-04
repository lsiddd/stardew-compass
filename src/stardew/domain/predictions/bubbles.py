from dataclasses import replace
from collections.abc import Sequence
from ..errors import FeatureUnavailable
from ..models.predictions import BubbleEvent
from ..models.state import GameState
from ..models.game_data import GameData
from ..numeric import for_day, f32


def predict(state, name, map):
    """Calculate one location without I/O; RNG consumption follows the game."""
    save = getattr(state, "metadata", state)
    times_fished = (
        state.players[0].stats.get("timesFished", 0)
        if getattr(state, "players", ())
        else getattr(save, "times_fished", 0)
    )
    result, active = [], None
    festival = save.day in {
        "spring": (13, 24),
        "summer": (11, 28),
        "fall": (16, 27),
        "winter": (11, 25),
    }.get(save.season, ())
    for time in range(610, 2600, 10):
        if time % 100 >= 60:
            continue
        random = for_day(save, time, map.width)
        if active is None:
            if random.double() >= 0.5 or (
                name.startswith("Farm") and name != "Farm_Fishing"
            ):
                continue
            for _ in range(2):
                x, y = random.next(map.width), random.next(map.height)
                if not map.open_water(x, y) or map.property(x, y, "NoFishing"):
                    continue
                land = map.distance_to_land(x, y)
                if land <= 1 or land > 4:
                    continue
                kind = "Bubbles"
                if (
                    random.double() < 0.01
                    and save.days_played - 1 > 3
                    and name in ("Town", "Mountain", "Forest", "Beach")
                    and time < 2300
                    and (times_fished > 2 or save.days_played - 1 > 14)
                    and not festival
                ):
                    random.double()
                    kind = "Frenzy"
                active = BubbleEvent(name, x, y, time, None, kind)
                break
        else:
            duration = (
                time // 100 * 60
                + time % 100
                - (active.start // 100 * 60 + active.start % 100)
            )
            if random.double() < 0.1 + f32(f32(duration) / 1800) and duration > (
                90 if active.kind == "Frenzy" else 60
            ):
                result.append(replace(active, end=time))
                active = None
    if active is not None:
        result.append(active)
    return result


DEFAULT_LOCATIONS = (
    "Town",
    "Mountain",
    "Forest",
    "Beach",
    "Desert",
    "Woods",
    "IslandNorth",
    "IslandWest",
    "IslandSouthEast",
)


def validate(state) -> None:
    """Apply requirements to bubbles only, leaving other analyses available."""
    save = getattr(state, "metadata", state)
    try:
        version = tuple(int(part) for part in save.game_version.split("."))
    except (AttributeError, ValueError) as error:
        raise FeatureUnavailable("Bubbles require a saved game version.") from error
    if not (1, 6, 9) <= version < (1, 7):
        raise FeatureUnavailable("Bubbles support the 1.6.9–1.6.x rules only.")
    for field in (
        "game_id",
        "days_played",
        "use_legacy_random",
        "season",
        "day",
        "year",
        "farm_type",
    ):
        if getattr(save, field, None) is None:
            raise FeatureUnavailable(f"Bubbles require saved {field}.")


def predict_bubbles(
    state: GameState, data: GameData, locations: Sequence[str] | None = None
) -> tuple[BubbleEvent, ...]:
    validate(state)
    available = DEFAULT_LOCATIONS + (
        ("Farm_Fishing",) if state.metadata.farm_type == 1 else ()
    )
    names = tuple(locations) if locations is not None else available
    unknown = set(names) - set(available)
    if unknown:
        raise FeatureUnavailable(
            "Unsupported bubble location: " + ", ".join(sorted(unknown))
        )
    events = []
    for name in names:
        if name not in data.maps:
            raise ValueError(f"Map resource missing: {name}")
        events.extend(predict(state, name, data.maps[name]))
    return tuple(sorted(events, key=lambda event: (event.start, event.location)))
