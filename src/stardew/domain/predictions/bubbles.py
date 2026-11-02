"""Fishing splash forecasts, including session-dependent frenzy alternatives."""

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass, replace

from ..errors import FeatureUnavailable
from ..models.game_data import GameData
from ..models.predictions import BubbleEvent
from ..models.state import GameState
from ..numeric import f32, for_day
from ..values import GameVersion

_SEASONS = ("spring", "summer", "fall", "winter")
_MAX_SCENARIOS = 64


@dataclass(frozen=True, slots=True)
class _Scenario:
    active: BubbleEvent | None = None
    completed: tuple[BubbleEvent, ...] = ()
    decisions: tuple[tuple[int, bool], ...] = ()


def _scenario_label(decisions):
    return "; ".join(
        f"{time // 100:02}:{time % 100:02}: "
        + ("eligible frenzy fish selected" if accepted else "no eligible frenzy fish")
        for time, accepted in decisions
    )


def predict(state, name, map):
    """Forecast each possible timeline; getFish uses an unavailable session RNG."""
    save = getattr(state, "metadata", state)
    players = getattr(state, "players", ())
    fish_caught_count = (
        len(players[0].collections.get("fishCaught", {}))
        if players
        else getattr(save, "fish_caught_count", None)
    )
    total_days = (save.year - 1) * 112 + _SEASONS.index(save.season) * 28 + save.day - 1
    if 3 < total_days <= 14 and fish_caught_count is None:
        raise FeatureUnavailable(
            "Early frenzy forecasts require the number of distinct fish caught."
        )
    eligible = total_days > 14 or (fish_caught_count or 0) > 2
    festival = save.day in {
        "spring": (13, 24),
        "summer": (11, 28),
        "fall": (16, 27),
        "winter": (11, 25),
    }.get(save.season, ())
    occupied = set()
    for location in getattr(getattr(state, "world", None), "locations", ()):
        if location.name == ("Farm" if name == "Farm_Fishing" else name):
            occupied.update((item.x, item.y) for item in location.objects)
    scenarios = [_Scenario()]
    for time in range(610, 2600, 10):
        if time % 100 >= 60:
            continue
        following = []
        for scenario in scenarios:
            random = for_day(save, time, map.width)
            active = scenario.active
            if active is not None:
                duration = (
                    time // 100 * 60
                    + time % 100
                    - (active.start // 100 * 60 + active.start % 100)
                )
                if random.double() < 0.1 + f32(f32(duration) / 1800) and duration > (
                    120 if active.kind == "Frenzy" else 60
                ):
                    scenario = replace(
                        scenario,
                        active=None,
                        completed=(*scenario.completed, replace(active, end=time)),
                    )
                following.append(scenario)
                continue
            if random.double() >= 0.5 or (
                name.startswith("Farm") and name != "Farm_Fishing"
            ):
                following.append(scenario)
                continue
            branched = False
            for _ in range(2):
                x, y = random.next(map.width), random.next(map.height)
                if (
                    (x, y) in occupied
                    or not map.open_water(x, y)
                    or map.property(x, y, "NoFishing")
                ):
                    continue
                land = map.distance_to_land(x, y)
                if land <= 1 or land > 4:
                    continue
                event = BubbleEvent(name, x, y, time, None, "Bubbles")
                if (
                    random.double() < (0.008 if name == "Beach" else 0.01)
                    and total_days > 3
                    and name in ("Town", "Mountain", "Forest", "Beach")
                    and time < 2300
                    and eligible
                    and not festival
                ):
                    # The seeded draw is only the getFish argument. Its result is
                    # selected by Game1.random and may be trash or a legendary fish.
                    random.next(500)
                    for accepted in (False, True):
                        following.append(
                            replace(
                                scenario,
                                active=replace(
                                    event, kind="Frenzy" if accepted else "Bubbles"
                                ),
                                decisions=(*scenario.decisions, (time, accepted)),
                            )
                        )
                    branched = True
                else:
                    scenario = replace(scenario, active=event)
                break
            if not branched:
                following.append(scenario)
        scenarios = following
        if len(scenarios) > _MAX_SCENARIOS:
            raise FeatureUnavailable(
                f"{name}: more than {_MAX_SCENARIOS} possible frenzy timelines; "
                "session observations are needed to narrow the forecast."
            )
    occurrences = defaultdict(list)
    for scenario in scenarios:
        events = scenario.completed + ((scenario.active,) if scenario.active else ())
        for event in events:
            occurrences[event].append(scenario.decisions)
    result = []
    for event, decisions in occurrences.items():
        if len(decisions) == len(scenarios):
            result.append(event)
        else:
            result.extend(
                replace(event, scenario=_scenario_label(choice)) for choice in decisions
            )
    return sorted(result, key=lambda e: (e.start, e.x, e.y, e.scenario or "", e.kind))


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
        inspected = GameVersion.parse(save.game_version) == GameVersion.parse("1.6.15")
    except (AttributeError, TypeError, ValueError) as error:
        raise FeatureUnavailable("Bubbles require a saved game version.") from error
    if not inspected:
        raise FeatureUnavailable(
            "Bubble rules have only been inspected for game 1.6.15."
        )
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
    names = tuple(dict.fromkeys(locations)) if locations is not None else available
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
