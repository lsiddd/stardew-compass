"""Literal port of the existing 1.6.15 artifact rules and their known limits."""

from __future__ import annotations

from dataclasses import dataclass, replace
from collections.abc import Mapping, Sequence
from ..errors import FeatureUnavailable
from ..models.predictions import DigItem, ArtifactResult
from ..models import SaveMetadata
from ..models.state import GameState
from ..models.game_data import GameData
from ..numeric import for_day, f32, i32


@dataclass(frozen=True, slots=True)
class ArtifactSpot:
    location: str
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class ArtifactState:
    save: SaveMetadata
    spots: tuple[ArtifactSpot, ...]
    mail: frozenset[str]
    orders: frozenset[str]
    order_rules: frozenset[str]
    dug: int = 0
    totems: int = 0
    lost_books: int = 0
    daily_luck: float = 0
    luck_level: int = 0
    mining_level: int = 0
    farming_mastery: bool = False
    golden_coconut_cracked: bool = False
    bridge_fixed: bool = False
    generous: bool = False
    archaeologist: bool = False

    @classmethod
    def from_game_state(cls, state: GameState) -> ArtifactState:
        """Extract only artifact inputs from the shared immutable saved state."""
        save, root, player = state.metadata, state.snapshot, state.player
        if save.game_version != "1.6.15":
            raise FeatureUnavailable(
                "Artifact rules have only been inspected for game 1.6.15."
            )
        for field in (
            "game_id",
            "days_played",
            "farm_type",
            "use_legacy_random",
            "daily_luck",
            "season",
            "day",
            "year",
        ):
            if getattr(save, field, None) is None:
                raise FeatureUnavailable(f"Artifacts require saved {field}.")
        hoes = [item for item in player.inventory if item.item_id == "Hoe"]
        if len(hoes) != 1:
            raise FeatureUnavailable(
                "Artifact prediction requires exactly one hoe in inventory."
            )
        enchantments = hoes[0].enchantments
        locations = root.findall("locations/*")
        spots = tuple(
            ArtifactSpot(
                location.value("name"),
                int(entry.value("key/Vector2/X")),
                int(entry.value("key/Vector2/Y")),
            )
            for location in locations
            for entry in location.findall("objects/item")
            if entry.value("value/Object/itemId") == "590"
        )
        orders = tuple(
            order
            for order in root.findall("specialOrders/*")
            if order.value("questState") == "InProgress"
        )
        return cls(
            save,
            spots,
            player.mail,
            frozenset(order.value("questKey", "") for order in orders),
            frozenset(
                rule
                for order in orders
                for rule in order.value("specialRule", "").split(",")
            ),
            player.stats.get("ArtifactSpotsDug", 0),
            state.world.treasure_totems_used or 0,
            state.world.lost_books_found or 0,
            save.daily_luck,
            player.skills.get("luck") or 0,
            player.skills.get("mining") or 0,
            player.stats.get("mastery_0", 0) > 0,
            state.world.golden_coconut_cracked is True,
            any(
                location.value("name") == "IslandNorth"
                and location.value("bridgeFixed") == "true"
                for location in locations
            ),
            "GenerousEnchantment" in enchantments,
            "ArchaeologistEnchantment" in enchantments,
        )


def next_bool(random, chance):
    return chance >= 1 or random.double() < chance


def condition(expression, state, spot, random):
    if not expression:
        return True
    for clause in expression.split(","):
        clause = clause.strip()
        negate = clause.startswith("!")
        args = (clause[1:] if negate else clause).split()
        key = args[0]
        if key == "PLAYER_LOCATION_NAME":
            value = spot.location == args[2]
        elif key == "LOCATION_SEASON":
            value = (
                "summer" if spot.location.startswith("Island") else state.save.season
            ).lower() == args[2].lower()
        elif key == "RANDOM":
            value = random.double() < float(args[1])
        elif key == "DAYS_PLAYED":
            value = state.save.days_played >= int(args[1])
        elif key == "PLAYER_HAS_MAIL":
            value = args[2] in state.mail
        elif key == "PLAYER_SPECIAL_ORDER_ACTIVE":
            value = args[2] in state.orders
        elif key == "PLAYER_SPECIAL_ORDER_RULE_ACTIVE":
            value = args[2] in state.order_rules
        elif key == "IS_ISLAND_NORTH_BRIDGE_FIXED":
            value = state.bridge_fixed
        elif key == "PLAYER_LUCK_LEVEL":
            value = state.luck_level >= int(args[2])
        elif key == "PLAYER_MINING_LEVEL":
            value = state.mining_level >= int(args[2])
        else:
            raise ValueError(f"Unsupported condition: {clause}")
        if value == negate:
            return False
    return True


def stack(drop, state, spot, random):
    low, high = drop["MinStack"], drop["MaxStack"]
    count = (
        random.next(max(low, 1), max(high, max(low, 1)) + 1)
        if high > 1
        else max(low, 1)
    )
    for modifier in drop["StackModifiers"] or []:
        if condition(modifier.get("Condition"), state, spot, random):
            if modifier["Modification"] != 0:
                raise ValueError("Unsupported stack modifier.")
            count = i32(count + int(modifier["Amount"]))
    return count


def cosmetic(r):
    if r.double() < 0.2:
        if r.double() < 0.05:
            return "(F)1369"
        choice = r.next(3)
        if choice == 0:
            choice = r.next(3)
            value = (
                r.next(10) * 3
                if choice == 0
                else r.next(1376, 1391)
                if choice == 1
                else r.next(6) * 2 + 1391
            )
        elif choice == 1:
            value = r.next(1362, 1370)
        else:
            value = r.next(1376, 1391)
        return "(F)" + str(value)
    if r.double() < 0.25:
        hats = [
            45,
            46,
            47,
            49,
            52,
            53,
            54,
            55,
            57,
            58,
            59,
            62,
            63,
            68,
            69,
            70,
            84,
            85,
            87,
            88,
            89,
            90,
        ]
        return "(H)" + str(hats[r.next(len(hats))])
    excluded = {
        1038,
        1041,
        1129,
        1130,
        1132,
        1133,
        1136,
        1152,
        1176,
        1177,
        1201,
        1202,
        1127,
    }
    while True:
        shirt = r.next(1112, 1291)
        if shirt not in excluded:
            return "(S)" + str(shirt)


class ArtifactPredictor:
    def __init__(self, tables):
        """Tables are loaded once by infrastructure and injected into the rules."""
        if not tables:
            raise FeatureUnavailable(
                "Artifacts require exported Locations, Objects and ObjectNames tables."
            )
        try:
            self.locations, self.objects, self.names = (
                tables[name] for name in ("Locations", "Objects", "ObjectNames")
            )
        except KeyError as error:
            raise FeatureUnavailable(
                "Artifacts require exported Locations, Objects and ObjectNames tables."
            ) from error

    def display_name(self, id):
        if id.startswith("runtime:"):
            return "Secret note OR stone (session RNG)"
        item = self.objects.get(id[3:]) if id.startswith("(O)") else None
        if item is None:
            return id
        display = item.get("DisplayName") or ""
        prefix = "[LocalizedText Strings\\Objects:"
        return (
            self.names[display[len(prefix) : -1]]
            if display.startswith(prefix) and display[len(prefix) : -1] in self.names
            else item.get("Name", id)
        )

    def resolve(self, query, state, spot, random):
        if query.startswith("LOST_BOOK_OR_ITEM "):
            return "(O)102" if state.lost_books < 21 else query[18:]
        if query.startswith("SECRET_NOTE_OR_ITEM "):
            return (
                "runtime:secret-note-or-stone"
                if "HasMagnifyingGlass" in state.mail
                or spot.location.startswith("Island")
                else query[20:]
            )
        if query == "RANDOM_ARTIFACT_FOR_DIG_SPOT":
            for id, item in self.objects.items():
                chances = item.get("ArtifactSpotChances")
                if (
                    item.get("Type") == "Arch"
                    and isinstance(chances, Mapping)
                    and spot.location in chances
                ):
                    if next_bool(
                        random,
                        f32(
                            (2 if state.archaeologist else 1)
                            * f32(chances[spot.location])
                        ),
                    ):
                        return "(O)" + id
            return None
        if not query.startswith("("):
            raise ValueError(f"Unsupported item query: {query}")
        return query

    def predict(self, state, spot):
        save, items = state.save, []

        def add(id, count=1, uncertain=False):
            alternatives = (
                (
                    ("(O)842", "(O)390")
                    if spot.location.startswith("Island")
                    else ("(O)79", "(O)390")
                )
                if uncertain
                else ()
            )
            items.append(
                DigItem(id, self.display_name(id), count, uncertain, alternatives)
            )

        defense = for_day(
            save, i32(-spot.x * 7), i32(spot.y * 777), i32(state.totems * 777)
        )
        dug = i32(state.dug + 1)
        if dug > 2 and defense.double() < 0.008 + (
            0.005 if "DefenseBookDropped" in state.mail else dug * 0.002
        ):
            add("(O)Book_Defense")
        if spot.location.startswith("Island"):
            r = for_day(save, i32(spot.x * 2000), spot.y)
            if state.golden_coconut_cracked and r.double() < 0.1:
                add("(O)791")
            elif r.double() < 0.33:
                add("(O)831", r.next(2, 5))
            elif r.double() < 0.15:
                add("(O)275", r.next(1, 3))
        random = for_day(save, i32(spot.x * 2000), spot.y, i32(state.totems * 777))
        if "sawQiPlane" in state.mail and random.double() < 0.05 + state.daily_luck / 2:
            add("(O)MysteryBox", random.next(1, 3))
        if state.farming_mastery and random.double() < 0.009 * (1 + state.daily_luck):
            add("(O)GoldenAnimalCracker")
        if save.days_played > 2 and random.double() < 0.018:
            add(cosmetic(random))
        if save.days_played > 2 and random.double() < 0.0054:
            add("(O)SkillBook_" + str(random.next(5)))
        location_key = spot.location
        if location_key == "Farm":
            farms = [
                "Standard",
                "Riverland",
                "Forest",
                "Hilltop",
                "Wilderness",
                "FourCorners",
                "Beach",
                "Meadowlands",
            ]
            if not 0 <= save.farm_type < len(farms):
                raise ValueError("Unsupported farm type.")
            location_key = "Farm_" + farms[save.farm_type]
        if location_key not in self.locations:
            raise ValueError(f"No drop table for {location_key}.")
        drops = (
            self.locations["Default"]["ArtifactSpots"]
            + self.locations[location_key]["ArtifactSpots"]
        )
        for drop in sorted(drops, key=lambda d: d["Precedence"]):
            if not next_bool(random, drop["Chance"]) or not condition(
                drop.get("Condition"), state, spot, random
            ):
                continue
            query = drop.get("ItemId")
            choices = drop["RandomItemId"]
            if isinstance(choices, (list, tuple)) and choices:
                query = choices[random.next(len(choices))]
            id = self.resolve(query, state, spot, random)
            if id is None:
                continue
            uncertain = id.startswith("runtime:")
            add(id, stack(drop, state, spot, random), uncertain)
            if (
                state.generous
                and drop["ApplyGenerousEnchantment"]
                and random.double() < 0.5
            ):
                add(id, stack(drop, state, spot, random), uncertain)
            if not drop["ContinueOnDrop"]:
                break
        note = (
            "Saved festival map; available only during the festival."
            if spot.location == "DesertFestival"
            else None
        )
        if any(i.runtime_dependent for i in items):
            note = (
                "Note or stone depends on session RNG, which is not stored in the save."
            )
        grouped = {}
        for item in items:
            key = (item.item_id, item.name, item.runtime_dependent)
            if key in grouped:
                grouped[key] = replace(
                    grouped[key], quantity=grouped[key].quantity + item.quantity
                )
            else:
                grouped[key] = item
        return ArtifactResult(
            spot.location, spot.x, spot.y, tuple(grouped.values()), note
        )


def predict_artifacts(
    state: GameState, data: GameData, locations: Sequence[str] | None = None
) -> tuple[ArtifactResult, ...]:
    context = ArtifactState.from_game_state(state)
    predictor = ArtifactPredictor(data.artifact_tables)
    names = frozenset(locations) if locations is not None else None
    return tuple(
        predictor.predict(context, spot)
        for spot in context.spots
        if names is None or spot.location in names
    )
