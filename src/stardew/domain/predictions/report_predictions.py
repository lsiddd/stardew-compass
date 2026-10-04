"""Structured analysis for the report's twenty-two prediction features."""

from collections.abc import Mapping, Sequence
from typing import Any
import re
from stardew.domain.errors import FeatureUnavailable
from stardew.domain.models.state import GameState
from stardew.domain.models.game_data import GameData
from . import report_rules as rules
from .report_models import (
    ReportPredictionOptions,
    PredictionDate,
    PredictionFact,
    PredictionAlternative,
    PredictionRecord,
    PredictionSection,
)

PredictionOptions = ReportPredictionOptions
SECTION_IDS = (
    "mines",
    "cart",
    "geode",
    "mystery",
    "train",
    "night",
    "crane",
    "krobus",
    "sandy",
    "wallpaper",
    "trash",
    "enchant",
    "minechest",
    "gembirds",
    "winterstar",
    "makeover",
    "greenrain",
    "cj",
    "book",
    "statue",
    "prize",
    "raccoon",
)
TITLES = (
    "Mines",
    "Traveling Cart",
    "Geodes",
    "Mystery Boxes",
    "Trains",
    "Night Events",
    "Crane Game",
    "Krobus",
    "Sandy",
    "Wallpaper",
    "Garbage Cans",
    "Enchantments",
    "Mine Chests",
    "Gem Birds",
    "Winter Star",
    "Desert Festival",
    "Weather",
    "Calico Jack",
    "Bookseller",
    "Statue Blessings",
    "Prize Tickets",
    "Raccoon Requests",
)
FUNCTIONS = (
    rules.predict_mines,
    rules.predict_cart,
    rules.predict_geodes,
    rules.predict_mystery_boxes,
    rules.predict_trains,
    rules.predict_night,
    rules.predict_crane,
    rules.predict_krobus,
    rules.predict_sandy,
    rules.predict_wallpaper,
    rules.predict_trash,
    rules.predict_enchantments,
    rules.predict_mine_chests,
    rules.predict_gem_birds,
    rules.predict_winter_star,
    rules.predict_makeover,
    rules.predict_green_rain,
    rules.predict_calico_jack,
    rules.predict_bookseller,
    rules.predict_statues,
    rules.predict_prize_ticket,
    rules.predict_raccoon,
)
PLAYER_SECTIONS = frozenset(("geode", "mystery", "enchant", "prize"))
SEQUENCE_SECTIONS = PLAYER_SECTIONS | {"raccoon"}
CALENDAR_SECTIONS = frozenset(
    ("mines", "trash", "train", "night", "crane", "greenrain", "statue")
)
MIN_VERSION = {
    "mystery": "1.6",
    "enchant": "1.5",
    "minechest": "1.5",
    "gembirds": "1.5",
    "makeover": "1.6",
    "greenrain": "1.6",
    "book": "1.6",
    "statue": "1.6",
    "prize": "1.6",
    "raccoon": "1.6",
    "crane": "1.4",
}


def _context_save(
    state: GameState, data: GameData, options: ReportPredictionOptions
) -> dict[str, Any]:
    player, metadata = state.player, state.metadata
    version = state.rules_version
    mail = player.mail
    values = {
        "gameID": metadata.game_id,
        "version": version,
        "daysPlayed": metadata.days_played,
        "year": metadata.year or 1,
        "dayAdjust": options.day_offset,
        "dailyLuck": max(
            -0.1,
            min(0.1, options.daily_luck if options.daily_luck is not None else -0.1),
        ),
        "luckLevel": options.luck_level,
        "useLegacyRandom": metadata.use_legacy_random or False,
        "seasonNames": ["Spring", "Summer", "Fall", "Winter"],
        "dayNames": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        "names": [p.name for p in state.players],
        "mp_ids": [p.player_id or 0 for p in state.players],
        "gender": [
            p.gender or ("Male" if p.is_male else "Female") for p in state.players
        ],
        "deepestMineLevel": player.deepest_mine_level or 0,
        "timesFedRaccoons": state.world.times_fed_raccoons or 0,
        "quarryUnlocked": "ccCraftsRoom" in mail,
        "desertUnlocked": "ccVault" in mail,
        "greenhouseUnlocked": "ccPantry" in mail,
        "theaterUnlocked": "ccMovieTheater" in mail
        and "ccMovieTheaterJoja" not in mail,
        "leoMoved": "leoMoved" in mail,
        "hasSpecialCharm": "HasSpecialCharm" in mail
        or player.has_special_charm is True,
        "gotMysteryBook": "GotMysteryBook" in mail,
        "hasGarbageBook": player.stats.get("Book_Trash", 0) > 0,
        "hardmodeMines": (state.world.mines_difficulty or 0) > 0,
        "hasFurnaceRecipe": "Furnace" in player.collections.get("craftingRecipes", {}),
        "visitsUntilY1Guarantee": (
            state.world.visits_until_y1_guarantee
            if state.world.visits_until_y1_guarantee is not None
            else -1
        ),
        "originalGuarantee": -1,
    }
    for key in (
        "geodesCracked",
        "MysteryBoxesOpened",
        "ticketPrizesClaimed",
        "timesEnchanted",
        "trashCansChecked",
    ):
        target = "mysteryBoxesOpened" if key == "MysteryBoxesOpened" else key
        values[target] = [p.stats.get(key, 0) for p in state.players]
    events = player.events
    values["ccComplete"], values["jojaComplete"] = (
        "191393" in events,
        "502261" in events,
    )
    values["qiCropsActive"] = state.world.qi_crops_active
    values["canHaveChildren"] = (
        rules.compare_version(version, "1.3") < 0
        and bool(player.spouse)
        and state.world.child_count < 2
    )
    if values["hasSpecialCharm"]:
        values["dailyLuck"] += 0.025
    mapping = {
        "cartItems": "cart_items_legacy",
        "cartItems_1_4": "cart_items_14",
        "cartFurniture": "cart_furniture",
        "geodeContents": "geode_contents",
        "wallpaperEquiv": "wallpaper_equivalents",
        "weapons": "weapons",
        "boots": "boots",
        "objects": "objects",
        "furniture": "furniture",
        "shirts": "shirts",
        "donatedItems": "donated_items",
    }
    for name, catalog in mapping.items():
        values[name] = rules.deepcopy(data.catalogs["predictor_" + catalog])
    values["characters"] = []
    exclusions = data.catalogs["predictor_friendship_exclusions"]
    for npc in state.world.npcs:
        name = npc.name
        if (
            not name
            or name in exclusions
            or any(kind in exclusions for kind in npc.traits)
        ):
            continue
        if name == "Leo" and not values["leoMoved"]:
            continue
        if name == "Sandy" and not values["desertUnlocked"]:
            continue
        if name == "Krobus" and (
            player.relationships.get("Krobus") is None
            or player.relationships["Krobus"].value("Friendship/Status") == "Unmet"
        ):
            continue
        values["characters"].append(name)
    for location in state.world.locations:
        for item_id in location.museum_items:
            entry = values["objects"].get("_" + item_id)
            if entry:
                values["donatedItems"][entry["name"]] = 1
    if rules.compare_version(version, "1.6") >= 0:
        values["geodeContents"]["275"].append("_Book_Artifact")
    prices = (
        {"_424": 160, "_426": 300, "_444": 100}
        if rules.compare_version(version, "1.1") < 0
        else {"_424": 200, "_426": 375}
        if rules.compare_version(version, "1.4") < 0
        else {"_444": 175}
        if rules.compare_version(version, "1.5") < 0
        else {"_251": 500, "_459": 200, "_773": 500}
        if rules.compare_version(version, "1.6") < 0
        else {}
    )
    for item_id, price in prices.items():
        values["objects"][item_id]["price"] = price
    guarantee = values["visitsUntilY1Guarantee"]
    day = (values["daysPlayed"] or 1) + values["dayAdjust"]
    if guarantee >= 0:
        values["originalGuarantee"] = (
            guarantee
            + day // 7
            + (day + 2) // 7
            + sum(day >= cutoff for cutoff in (99, 100, 101))
        )
    elif guarantee == -99:
        values["originalGuarantee"] = rules.SystemRandom(12 * values["gameID"]).next(
            2, 31
        )
    return values


def _snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _date(day):
    day = int(day)
    return PredictionDate(
        day,
        (day - 1) // 112 + 1,
        ("spring", "summer", "fall", "winter")[((day - 1) // 28) % 4],
        (day - 1) % 28 + 1,
    )


def _ids(data):
    result = {}
    ambiguous = set()
    for table, prefix in (("objects", "O"), ("shirts", "S"), ("furniture", "F")):
        for key, value in data.catalogs["predictor_" + table].items():
            if isinstance(value, Mapping):
                name, identifier = (
                    value.get("name"),
                    value.get("id", key.removeprefix("_")),
                )
                if name:
                    qualified = f"({prefix}){identifier}"
                    if name in result and result[name] != qualified:
                        ambiguous.add(name)
                    else:
                        result[name] = qualified
    for table, prefix in (("weapons", "W"), ("boots", "B")):
        for key, name in data.catalogs["predictor_" + table].items():
            if isinstance(name, str) and name not in result:
                result[name] = f"({prefix}){key}"
    return {
        name: identifier for name, identifier in result.items() if name not in ambiguous
    }


def _product_id(name, identities):
    if name in identities:
        return identities[name]
    if name.startswith("Smoked "):
        return "(O)SmokedFish"
    if name.startswith("Pickled "):
        return "(O)342"
    if name.endswith(" Juice"):
        return "(O)350"
    if name.endswith(" Jelly"):
        return "(O)344"
    if name.startswith("Dried "):
        return (
            "(O)DriedMushrooms"
            if "Mushroom" in name or name in ("Dried Morel", "Dried Chanterelle")
            else "(O)DriedFruit"
        )
    return None


def _records(section, context, data):
    identities = _ids(data)
    result = []
    for _, raw in context.captures:
        facts = dict(raw)
        day = facts.get("day")
        sequence = next(
            (
                facts[k]
                for k in (
                    "numCracked",
                    "numOpened",
                    "timesEnchanted",
                    "tableRow",
                    "numPlayed",
                )
                if facts.get(k) is not None
            ),
            None,
        )
        player_index = facts.get("whichPlayer", facts.get("player"))
        player_id = (
            context.save["mp_ids"][int(player_index)]
            if player_index is not None
            and 0 <= int(player_index) < len(context.save["mp_ids"])
            else None
        )
        location, item, quantity, price, alternatives = (
            None,
            facts.get("item"),
            facts.get("qty", facts.get("itemQty")),
            facts.get("price"),
            [],
        )
        if isinstance(item, Mapping):
            facts["item_id"] = item.get("item_id")
            item, quantity, price = (
                item.get("name"),
                item.get("qty", quantity),
                item.get("price", price),
            )
        if section in ("geode", "mystery"):
            column = int(facts["c"])
            item, quantity = facts["item"][column], facts["itemQty"][column]
            facts["item_id"] = facts.get("itemIDs", [None] * len(facts["item"]))[column]
            facts["container"] = (
                (
                    "Geode",
                    "Frozen Geode",
                    "Magma Geode",
                    "Omni Geode",
                    "Artifact Trove",
                    "Golden Coconut",
                )[column]
                if section == "geode"
                else (
                    "Mystery Box",
                    "Golden Mystery Box",
                    "Golden Mystery Box with Foraging Mastery",
                )[column]
            )
            if facts.get("couldBeBeansTrove" if column >= 4 else "couldBeBeans"):
                alternatives.append(
                    PredictionAlternative(
                        "Qi crop challenge active; session RNG determines quantity",
                        "(O)890",
                        "Qi Bean",
                        None,
                    )
                )
            if column == 5 and facts.get("couldBeHat"):
                alternatives.append(
                    PredictionAlternative(
                        "First eligible golden coconut", "(H)75", "Golden Helmet", 1
                    )
                )
        elif section == "trash":
            item = facts.get("trashItem")
            quantity = facts.get("stack") or 1
            location = (
                "Jodi",
                "Emily",
                "Mayor",
                "Museum",
                "Blacksmith",
                "Saloon",
                "Alex",
                "Joja",
            )[int(facts["whichCan"])]
        elif section == "train":
            facts["arrives"] = bool(
                facts.get("thisTrain") and "Train at" in facts["thisTrain"]
            )
        elif section == "night" or section == "crane":
            facts["event"] = facts.get("thisEvent")
        elif section == "krobus":
            column = int(facts["i"])
            day = context.save["_calculation_offset"] + (3, 6)[column]
            item, quantity, price = (
                facts["item"][column],
                facts["qty"][column],
                facts["price"][column],
            )
            facts["item_id"] = facts.get("itemIDs", [None, None])[column]
        elif section == "cart" and isinstance(item, (list, tuple)):
            item, quantity, price = item
            day = facts.get("startDay")
        elif section == "sandy":
            item = item.split(" ID:")[0]
            facts["item_id"] = f"(S){facts['numID']}"
        elif section == "gembirds":
            index = int(facts["i"])
            location = facts["locs"][index]
            facts = {
                "direction": location,
                "bird": facts["birds"][index],
                "gem": facts["gems"][facts["birds"][index]],
            }
            item = facts["gem"]
        elif section == "makeover":
            if facts.get("d") is not None:
                day = facts.get("day")
                if "racers" in facts:
                    facts = {
                        "racers": facts["racers"][str(facts["d"])],
                        "vendors": tuple(
                            facts["vendor"][str(slot)][int(facts["d"])]
                            for slot in (1, 2)
                        ),
                    }
            elif "parts" in facts:
                facts["kind"] = "cactus"
        elif section == "wallpaper":
            for location, wall, flooring, equivalent, available in (
                (
                    "Pierre",
                    facts["wp_p"],
                    facts["fl_p"],
                    facts["eq_p"],
                    context.save["ccComplete"] or (int(day) - 1) % 7 != 2,
                ),
                (
                    "JojaMart",
                    facts["wp_j"],
                    facts["fl_j"],
                    facts["eq_j"],
                    not context.save["ccComplete"],
                ),
            ):
                if not available:
                    result.append(
                        PredictionRecord(
                            date=_date(day),
                            location=location,
                            facts=(PredictionFact("open", False),),
                        )
                    )
                    continue
                for kind, number in (("Wallpaper", wall), ("Flooring", flooring)):
                    result.append(
                        PredictionRecord(
                            date=_date(day),
                            location=location,
                            item_name=kind,
                            quantity=1,
                            facts=(
                                PredictionFact("texture_id", int(number) - 1),
                                PredictionFact("display_number", int(number)),
                                PredictionFact(
                                    "equivalent_item",
                                    equivalent if kind == "Wallpaper" else None,
                                ),
                            ),
                        )
                    )
            continue
        elif section == "statue":
            if "coords" in facts:
                location = facts["pbMaps"][int(facts["index"])]
                facts = {
                    "coordinate_candidates": facts["coords"],
                    "prismatic_shard": facts["shard"],
                    "requires_clear_spawn_tile": True,
                }
            else:
                facts = {
                    "blessing_rain": facts["blessingNames"][int(facts["blessRain"])],
                    "blessing_clear": facts["blessingNames"][int(facts["blessNoRain"])],
                    "dwarf_choices": (
                        facts["dwarfNames"][int(facts["dwarf1"])],
                        facts["dwarfNames"][int(facts["dwarf2"])],
                    ),
                }
        elif section == "raccoon":
            for slot in range(3):
                name, amount = facts["bundleItem"][slot], facts["bundleQty"][slot]
                seasonal = ()
                if isinstance(name, (list, tuple)):
                    seasonal = tuple(
                        PredictionAlternative(
                            f"Season: {season}",
                            _product_id(choice, identities),
                            choice,
                            int(amount) if str(amount).isdigit() else None,
                        )
                        for season, choice in zip(
                            ("spring", "summer", "fall", "winter"), name
                        )
                    )
                    name = None
                if isinstance(name, str) and " OR " in name:
                    seasonal = tuple(
                        PredictionAlternative(
                            "Depends on unshipped collections",
                            _product_id(choice, identities),
                            choice,
                            int(quantity),
                        )
                        for choice, quantity in zip(
                            name.split(" OR "), str(amount).split(" OR ")
                        )
                    )
                    name = None
                result.append(
                    PredictionRecord(
                        sequence=int(sequence),
                        item_id=_product_id(name, identities) if name else None,
                        item_name=name,
                        quantity=int(amount) if str(amount).isdigit() else None,
                        alternatives=seasonal,
                        facts=(
                            PredictionFact("role", "request" if slot < 2 else "reward"),
                            PredictionFact("slot", slot + 1),
                        ),
                    )
                )
            continue
        elif section == "winterstar":
            day = (int(facts["year"]) - 1) * 112 + 109
        elif section == "enchant":
            for tool_index, tool in enumerate(facts["labels"]):
                pool = facts["validEnchants"][tool_index]
                roll = facts["randRoll"]
                selected = facts["item"][tool_index][0]
                conditional = []
                for previous_index, previous in enumerate(pool):
                    second_index = int(roll * (len(pool) - 1))
                    if previous_index <= second_index:
                        second_index += 1
                    third_index = int(roll * (len(pool) - 2))
                    if previous_index <= third_index:
                        third_index += 1
                    if second_index == third_index:
                        third_index += 1
                        if previous_index == third_index:
                            third_index += 1
                    conditional.extend(
                        PredictionAlternative(
                            f"Previous enchantment: {previous}", None, pool[index]
                        )
                        for index in (second_index, third_index)
                    )
                result.append(
                    PredictionRecord(
                        sequence=int(sequence),
                        player_id=player_id,
                        item_name=selected,
                        alternatives=tuple(conditional),
                        facts=(
                            PredictionFact("tool", tool),
                            PredictionFact("fresh_enchantment", selected),
                        ),
                    )
                )
            continue
        elif section == "book":
            for index, visit in enumerate(facts["days"]):
                for slot, stock in facts["stock"][str(index)].items():
                    if stock:
                        name, cost = stock["name"], stock["price"]
                        result.append(
                            PredictionRecord(
                                date=_date(context.save["_calculation_offset"] + visit),
                                item_id=identities.get(name),
                                item_name=name,
                                quantity=1,
                                price=cost,
                                facts=(PredictionFact("slot", _snake(slot)),),
                            )
                        )
            continue
        time = (
            int(facts["trainTime"])
            if section == "train" and facts.get("arrives")
            else None
        )
        if section == "trash" and isinstance(item, str):
            match = re.fullmatch(r"(.*) x(\d+)", item)
            if match:
                item, quantity = match[1], int(match[2])
        if isinstance(price, str) and price.endswith("g"):
            price = int(price[:-1].replace(",", ""))
        if isinstance(item, str) and " or " in item:
            choices = item.split(" or ")
            item = choices[0]
            alternatives.extend(
                PredictionAlternative(
                    "Session RNG or save-dependent alternative",
                    identities.get(name),
                    name,
                    quantity if isinstance(quantity, int) else None,
                )
                for name in choices[1:]
            )
        if isinstance(item, str) and item.endswith(" or Qi Bean (1 or 5)"):
            item = item.removesuffix(" or Qi Bean (1 or 5)")
        result.append(
            PredictionRecord(
                date=_date(day) if day is not None else None,
                sequence=int(sequence) if sequence is not None else None,
                player_id=player_id,
                location=location,
                time=time,
                item_id=facts.get("item_id")
                or (
                    "(O)390"
                    if item == "Stone" and section in ("geode", "mystery")
                    else identities.get(item)
                )
                if isinstance(item, str)
                else None,
                item_name=item if isinstance(item, str) else None,
                quantity=int(quantity) if isinstance(quantity, (int, float)) else None,
                price=int(price) if isinstance(price, (int, float)) else None,
                alternatives=tuple(alternatives),
                facts=tuple(
                    PredictionFact(_snake(key), rules.immutable_fact(value))
                    for key, value in facts.items()
                ),
            )
        )
    return result


def analyze_predictions(
    state: GameState,
    data: GameData,
    sections: Sequence[str] | None = None,
    options: ReportPredictionOptions | Mapping[str, Any] | None = None,
) -> tuple[PredictionSection, ...]:
    options = options or PredictionOptions()
    if isinstance(options, Mapping):
        options = PredictionOptions(**options)
    if not isinstance(options, PredictionOptions):
        raise TypeError("prediction options must be PredictionOptions or a mapping")
    selected = SECTION_IDS if sections is None else tuple(sections)
    unknown = set(selected) - set(SECTION_IDS)
    if unknown:
        raise ValueError("Unknown prediction sections: " + ", ".join(sorted(unknown)))
    if not selected:
        return ()
    save = _context_save(state, data, options)
    results = []
    for section in selected:
        index = SECTION_IDS.index(section)
        diagnostics = []
        minimum = MIN_VERSION.get(section)
        if minimum and rules.compare_version(save["version"], minimum) < 0:
            diagnostics.append(
                f"{TITLES[index]} requires game version {minimum} or later."
            )
        if (
            section not in ("minechest", "gembirds", "winterstar", "makeover")
            and save["daysPlayed"] is None
        ):
            diagnostics.append(
                "Save does not contain days_played; prediction dates cannot be calculated."
            )
        if section == "makeover" and len(save["characters"]) < 6:
            diagnostics.append(
                "Desert Festival vendor predictions require the saved NPC pool."
            )
        if diagnostics:
            if sections is not None and len(selected) == 1:
                raise FeatureUnavailable(diagnostics[0])
            results.append(
                PredictionSection(section, TITLES[index], (), tuple(diagnostics), False)
            )
            continue
        players = (
            options.player_indices
            if options.player_indices is not None
            else tuple(range(len(state.players)))
            if section in PLAYER_SECTIONS
            else (0,)
        )
        if any(player < 0 or player >= len(state.players) for player in players):
            raise ValueError("Prediction player index is outside the save player list.")
        records = []
        requested_day = (
            options.start if options.start is not None else save["daysPlayed"]
        )
        explicit_interval = options.start is not None or options.count is not None
        if section == "mines" and explicit_interval:
            offsets = (None,)
        elif section in CALENDAR_SECTIONS and explicit_interval:
            first = ((requested_day - 1) // 28) * 28
            last = requested_day + (options.count or 28) - 1
            offsets = range(first, last, 28)
        elif section in ("cart", "krobus", "sandy", "wallpaper") and explicit_interval:
            first = ((requested_day - 1) // 7) * 7
            last = requested_day + (options.count or 7) - 1
            offsets = list(range(first, last, 7))
            if section == "cart":
                for year in range(first // 112, last // 112 + 1):
                    extras = (
                        (10, 94)
                        if rules.compare_version(save["version"], "1.6") >= 0
                        else (94,)
                        if rules.compare_version(save["version"], "1.3") >= 0
                        else ()
                    )
                    offsets.extend(
                        year * 112 + day
                        for day in extras
                        if first <= year * 112 + day <= last
                    )
                offsets = sorted(set(offsets))
        elif section == "book" and explicit_interval:
            first = ((requested_day - 1) // 28) * 28
            last = requested_day + (options.count or 28) - 1
            offsets = range(first, last, 28)
        elif section in ("winterstar", "makeover") and explicit_interval:
            first = (options.start or save["year"]) - 1
            offsets = range(first, first + (options.count or 1))
        elif (
            section in SEQUENCE_SECTIONS
            and options.count is not None
            and options.start is None
        ):
            offsets = ("saved_counter",)
        elif options.start is not None:
            offsets = (
                options.start - 1 if section in SEQUENCE_SECTIONS else options.start,
            )
        else:
            offsets = (None,)
        for player_index in players:
            for offset in offsets:
                if offset == "saved_counter":
                    counter = {
                        "geode": "geodesCracked",
                        "mystery": "mysteryBoxesOpened",
                        "enchant": "timesEnchanted",
                        "prize": "ticketPrizesClaimed",
                        "raccoon": "timesFedRaccoons",
                    }[section]
                    saved = save[counter]
                    offset = saved[player_index] if isinstance(saved, list) else saved
                working = rules.deepcopy(save)
                working["_calculation_offset"] = (
                    offset
                    if offset is not None
                    else 28 * (working["daysPlayed"] // 28)
                    if section == "book"
                    else 7 * ((working["daysPlayed"] - 1) // 7)
                    if section in ("cart", "krobus", "sandy", "wallpaper")
                    else 0
                )
                context = rules.PredictionContext(
                    working, data.catalogs, player_index, options.count
                )
                if section == "mines" and explicit_interval:
                    context.day_range = (
                        requested_day,
                        requested_day + (options.count or 28),
                    )
                if section == "cj":
                    FUNCTIONS[index](context, False, offset, options.game_start - 1)
                else:
                    FUNCTIONS[index](context, False, offset)
                records.extend(_records(section, context, data))
        if explicit_interval and section in CALENDAR_SECTIONS | {
            "cart",
            "krobus",
            "sandy",
            "wallpaper",
            "book",
        }:
            width = options.count or (
                7 if section in ("cart", "krobus", "sandy", "wallpaper") else 28
            )
            records = [
                record
                for record in records
                if record.date
                and requested_day <= record.date.days_played < requested_day + width
            ]
        if options.item_filter:
            query = options.item_filter.casefold()
            records = [
                record
                for record in records
                if query in (record.item_name or "").casefold()
                or query in (record.item_id or "").casefold()
                or any(query in str(fact.value).casefold() for fact in record.facts)
            ]
        results.append(
            PredictionSection(
                section, TITLES[index], tuple(records), tuple(diagnostics)
            )
        )
    return tuple(results)
