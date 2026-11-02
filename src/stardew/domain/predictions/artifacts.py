"""Literal port of the existing 1.6.15 artifact rules and their known limits."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace

from ..errors import FeatureUnavailable
from ..models import SaveMetadata
from ..models.game_data import GameData
from ..models.predictions import ArtifactResult, DigItem
from ..models.state import GameState
from ..numeric import f32, for_day, i32
from ..values import GameVersion
from .artifact_conditions import compile_condition, validate_artifact_tables

# Vanilla map/context profiles inspected against 1.6.15 XNBs. Location names
# are identifiers, not a naming convention for inheritance or map properties.
_VALLEY_LOCATIONS = frozenset(
    "Farm FarmHouse FarmCave Town JoshHouse HaleyHouse SamHouse Blacksmith "
    "ManorHouse SeedShop Saloon Trailer Hospital HarveyRoom Beach BeachNightMarket "
    "ElliottHouse Mountain ScienceHouse SebastianRoom Tent Forest WizardHouse "
    "AnimalShop LeahHouse BusStop Mine Sewer BugLand ArchaeologyHouse "
    "WizardHouseBasement AdventureGuild Woods Railroad WitchSwamp WitchHut "
    "WitchWarpCave Summit FishShop BathHouse_Entry BathHouse_MensLocker "
    "BathHouse_WomensLocker BathHouse_Pool CommunityCenter JojaMart Greenhouse "
    "Backwoods Tunnel Trailer_Big Cellar MermaidHouse Submarine AbandonedJojaMart "
    "MovieTheater Sunroom BoatTunnel LeoTreeHouse MasteryCave LewisBasement".split()
)
_DESERT_LOCATIONS = frozenset(
    ("Desert", "Club", "SandyHouse", "SkullCave", "DesertFestival")
)
_ISLAND_LOCATIONS = frozenset(
    "IslandSouth IslandSouthEast IslandSouthEastCave IslandEast IslandWest "
    "IslandNorth IslandHut IslandWestCave1 IslandNorthCave1 IslandFieldOffice "
    "IslandFarmHouse CaptainRoom IslandShrine IslandFarmCave Caldera QiNutRoom".split()
)
_VANILLA_CONTEXT_SEASONS = {"Default": None, "Desert": "summer", "Island": "summer"}
_SEASONS = ("spring", "summer", "fall", "winter")


def location_context(name: str) -> str:
    if name in _VALLEY_LOCATIONS:
        return "Default"
    if name in _DESERT_LOCATIONS:
        return "Desert"
    if name in _ISLAND_LOCATIONS:
        return "Island"
    raise FeatureUnavailable(
        f"Artifact location context has not been inspected: {name}."
    )


def location_season(state: ArtifactState, spot: ArtifactSpot) -> str:
    context = location_context(spot.location)
    # These island maps have an explicit SeasonOverride map property, which
    # takes precedence over their LocationContexts entry.
    if spot.location in _ISLAND_LOCATIONS:
        return "summer"
    seasons = state.context_seasons
    if seasons is None:
        seasons = _VANILLA_CONTEXT_SEASONS
    if context not in seasons:
        raise FeatureUnavailable(f"Artifacts require the {context} location context.")
    return seasons[context] or state.save.season


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
    pending_mail: frozenset[str] = frozenset()
    unseen_notes: int | None = None
    unseen_journal: int | None = None
    assumptions: tuple[str, ...] = ()
    context_seasons: Mapping[str, str | None] | None = None

    @classmethod
    def from_game_state(
        cls, state: GameState, *, online_player_indices: Sequence[int] | None = None
    ) -> ArtifactState:
        """Extract only artifact inputs from the shared immutable saved state."""
        save, player = state.metadata, state.player
        try:
            inspected = GameVersion.parse(save.game_version) == GameVersion.parse(
                "1.6.15"
            )
        except (AttributeError, TypeError, ValueError):
            inspected = False
        if not inspected:
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
        if online_player_indices is None:
            if len(state.players) != 1:
                raise FeatureUnavailable(
                    "Artifact drops require the average luck of online players; "
                    "the save does not identify which multiplayer farmers are online."
                )
            online = (0,)
        else:
            online = tuple(online_player_indices)
            if (
                not online
                or 0 not in online
                or len(set(online)) != len(online)
                or any(
                    isinstance(i, bool)
                    or not isinstance(i, int)
                    or not 0 <= i < len(state.players)
                    for i in online
                )
            ):
                raise ValueError(
                    "Online player indices must be unique valid indices including the host digger (0)."
                )
        # FarmerTeam.AverageDailyLuck adds each online farmer in enumeration
        # order. Python 3.12+ sum uses compensated addition for floats, which
        # can change the final double and a later chance comparison.
        total_luck = 0.0
        for i in online:
            total_luck += min(
                f32(0.2),
                max(
                    -f32(0.2),
                    save.daily_luck
                    + (
                        f32(0.025)
                        if (
                            state.players[i].has_special_charm
                            or "HasSpecialCharm" in state.players[i].mail
                        )
                        else 0
                    ),
                ),
            )
        effective_luck = total_luck / len(online)
        pending_mail = frozenset(
            (node.text("") or "").removesuffix("%&NL&%")
            for path in ("mailbox/string", "mailForTomorrow/string")
            for node in player.snapshot.findall(path)
        )
        seen = {
            int(node.text("0"))
            for node in player.snapshot.findall("secretNotesSeen/int")
        }

        def notes_remaining(ids, item_id):
            return max(
                0,
                len(set(ids) - seen)
                - sum(
                    item.quantity or 0
                    for item in player.inventory
                    if item.item_id == item_id
                ),
            )

        for location in state.world.locations:
            if any(
                item.item_id == "590"
                and (location.name is None or item.x is None or item.y is None)
                for item in location.objects
            ):
                raise FeatureUnavailable(
                    "Artifacts require a saved location and coordinates for every dig spot."
                )
        spots = tuple(
            ArtifactSpot(location.name, item.x, item.y)
            for location in state.world.locations
            for item in location.objects
            if item.item_id == "590"
            and location.name is not None
            and item.x is not None
            and item.y is not None
        )
        return cls(
            save,
            spots,
            player.mail,
            state.world.active_order_keys,
            state.world.active_order_rules,
            player.stats.get("ArtifactSpotsDug", 0),
            state.world.treasure_totems_used or 0,
            state.world.lost_books_found or 0,
            effective_luck,
            player.skills.get("luck") or 0,
            player.skills.get("mining") or 0,
            player.stats.get("mastery_0", 0) > 0,
            state.world.golden_coconut_cracked is True,
            any(
                location.name == "IslandNorth" and location.bridge_fixed is True
                for location in state.world.locations
            ),
            "GenerousEnchantment" in enchantments,
            "ArchaeologistEnchantment" in enchantments,
            pending_mail=pending_mail,
            unseen_notes=notes_remaining(range(1, 28), "79"),
            unseen_journal=notes_remaining(range(1001, 1012), "842"),
            assumptions=(
                "Host's next dig; digging routes and future skill buffs are not simulated.",
                f"Average daily luck of selected online players: {effective_luck:.9g} (including Special Charm).",
            ),
        )


def next_bool(random, chance):
    return chance >= 1 or random.double() < chance


def condition(expression, state, spot, random):
    for clause in compile_condition(expression):
        key, negate = clause.key, clause.negate
        args = (key, *clause.arguments)
        if key == "PLAYER_LOCATION_NAME":
            value = spot.location.casefold() == args[2].casefold()
        elif key == "LOCATION_SEASON":
            value = location_season(state, spot).casefold() == args[2].casefold()
        elif key == "RANDOM":
            value = random.double() < f32(float(args[1]))
        elif key == "DAYS_PLAYED":
            value = state.save.days_played >= int(args[1])
        elif key == "PLAYER_HAS_MAIL":
            value = args[2] in state.mail or args[2] in state.pending_mail
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
    def __init__(self, tables, *, location_contexts=None):
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
        validate_artifact_tables(tables)
        self.context_seasons = None
        if location_contexts is not None:
            seasons = {}
            for name, data in location_contexts.items():
                if not isinstance(data, Mapping) or "SeasonOverride" not in data:
                    raise FeatureUnavailable(
                        f"Artifacts require SeasonOverride data for context {name}."
                    )
                value = data["SeasonOverride"]
                if value is not None and (
                    isinstance(value, bool)
                    or not isinstance(value, int)
                    or not 0 <= value < len(_SEASONS)
                ):
                    raise ValueError(f"Unsupported season override for context {name}.")
                seasons[name] = _SEASONS[value] if value is not None else None
            self.context_seasons = seasons
        self.drops = {
            name: tuple(
                sorted(
                    (
                        *self.locations["Default"]["ArtifactSpots"],
                        *location["ArtifactSpots"],
                    ),
                    key=lambda drop: drop["Precedence"],
                )
            )
            for name, location in self.locations.items()
        }
        self.artifacts_by_location = {}
        for identifier, item in self.objects.items():
            if item.get("Type") == "Arch":
                for location, chance in (item.get("ArtifactSpotChances") or {}).items():
                    self.artifacts_by_location.setdefault(location, []).append(
                        (identifier, chance)
                    )

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
            else item.get("Name") or id
        )

    def resolve(self, query, state, spot, random):
        if query.startswith("LOST_BOOK_OR_ITEM "):
            return "(O)102" if state.lost_books < 21 else query[18:]
        if query.startswith("SECRET_NOTE_OR_ITEM "):
            remaining = (
                state.unseen_journal
                if location_context(spot.location) == "Island"
                else state.unseen_notes
            )
            if remaining == 0:
                return query[20:]
            return (
                "runtime:secret-note-or-stone"
                if "HasMagnifyingGlass" in state.mail
                or location_context(spot.location) == "Island"
                else query[20:]
            )
        if query == "RANDOM_ARTIFACT_FOR_DIG_SPOT":
            for id, chance in self.artifacts_by_location.get(spot.location, ()):
                if next_bool(
                    random, f32((2 if state.archaeologist else 1) * f32(chance))
                ):
                    return "(O)" + id
            return None
        if not query.startswith("("):
            raise ValueError(f"Unsupported item query: {query}")
        return query

    def predict(self, state, spot):
        context = location_context(spot.location)
        if self.context_seasons is not None:
            state = replace(state, context_seasons=self.context_seasons)
        save, items = state.save, []
        if spot.location == "DesertFestival" and not (
            save.season == "spring" and 15 <= save.day <= 17
        ):
            return ArtifactResult(
                spot.location,
                spot.x,
                spot.y,
                (),
                "Inactive Desert Festival map; saved spots cannot be dug on this date. "
                "Their contents are not a forecast for the next festival.",
            )

        def add(id, count=1, uncertain=False):
            alternatives = (
                (("(O)842", "(O)390") if context == "Island" else ("(O)79", "(O)390"))
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
        if context == "Island" and spot.location != "IslandFarmHouse":
            r = for_day(save, i32(spot.x * 2000), spot.y)
            if state.golden_coconut_cracked and r.double() < 0.1:
                add("(O)791")
            elif r.double() < 0.33:
                add("(O)831", r.next(2, 5))
            elif r.double() < 0.15:
                add("(O)275", r.next(1, 3))
        elif spot.location == "DesertFestival":
            festival_random = for_day(save, i32(spot.x * 2000), spot.y)
            add("(O)CalicoEgg", festival_random.next(3, 7))
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
        for drop in self.drops[location_key]:
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
        note = " ".join(filter(None, (note, *state.assumptions))) or None
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
    state: GameState,
    data: GameData,
    locations: Sequence[str] | None = None,
    *,
    online_player_indices: Sequence[int] | None = None,
) -> tuple[ArtifactResult, ...]:
    context = ArtifactState.from_game_state(
        state, online_player_indices=online_player_indices
    )
    predictor = ArtifactPredictor(
        data.artifact_tables,
        location_contexts=data.catalogs.get("game_LocationContexts"),
    )
    names = frozenset(locations) if locations is not None else None
    return tuple(
        predictor.predict(context, spot)
        for spot in context.spots
        if names is None or spot.location in names
    )
