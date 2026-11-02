"""Normalize saved world and player facts for deterministic rule evaluation."""

from types import MappingProxyType
from typing import Any

from stardew.domain.models.game_data import GameData
from stardew.domain.models.state import GameState, freeze
from stardew.domain.numeric import f32

from . import report_support as rules
from .loot.tool_state import saved_enchantment_tools
from .report_models import ReportPredictionOptions


def _pending_mail(player):
    return frozenset(
        (node.text("") or "").split("%", 1)[0]
        for path in ("mailForTomorrow/string", "mailbox/string")
        for node in player.snapshot.findall(path)
    )


def _mail_for_tomorrow(player):
    """Night repair triggers use tomorrow's queue, excluding delivered mail."""
    return frozenset(
        (node.text("") or "").split("%", 1)[0]
        for node in player.snapshot.findall("mailForTomorrow/string")
    )


def _saved_int(node, path):
    value = node.value(path)
    return int(value) if value is not None else None


def _world_inputs(state, data):
    host = state.player
    mail = host.mail | _pending_mail(host)
    cc_areas = ("BoilerRoom", "CraftsRoom", "Pantry", "FishTank", "Vault")
    completed_areas = all("cc" + area in host.mail for area in cc_areas)
    joja_areas = all(
        "cc" + area in host.mail or "joja" + area in host.mail for area in cc_areas
    )
    root = state.snapshot
    theater = next((p for p in state.world.locations if p.name == "MovieTheater"), None)
    day = state.metadata.days_played
    weather = {}
    for entry in root.findall("locationWeather/item"):
        if entry.value("key/string") == "Default" and day is not None:
            for target, path in (
                (day, "weather/string"),
                (day + 1, "weatherForTomorrow/string"),
            ):
                value = entry.value("value/LocationWeather/" + path)
                if value:
                    weather[str(target)] = value
    source_hash = (
        data.provenance.get("game_tables", {})
        .get("sources", {})
        .get("Stardew Valley.dll", "")
        .lower()
    )
    priority = (
        "leoMoved",
        "jojaPantry",
        "ccPantry",
        "jojaVault",
        "ccVault",
        "jojaBoilerRoom",
        "ccBoilerRoom",
        "jojaCraftsRoom",
        "ccCraftsRoom",
        "jojaFishTank",
        "ccFishTank",
        "ccMovieTheaterJoja",
        "jojaMovieTheater",
        "ccMovieTheater",
    )
    pending = _mail_for_tomorrow(host)
    return {
        "game_profile": "installed-f3e97f01"
        if source_hash
        == "f3e97f01d3fd2b1e6094fc8d2b59950aa6cb9d6cd1bf1b39d72d58edda8aad12"
        else None,
        "shuffleMineChests": root.value("shuffleMineChests"),
        "lowestMineLevel": _saved_int(root, "mine_lowestLevelReached"),
        "lowestMineLevelForOrder": _saved_int(root, "mine_lowestLevelReachedForOrder"),
        "quarryMineVisited": "VisitedQuarryMine" in mail,
        "hostTheaterUnlocked": "ccMovieTheater" in host.mail
        and "ccMovieTheaterJoja" not in host.mail,
        "hostMailWithPending": mail,
        "hostMailReceived": host.mail,
        "hostCcCeremonySeen": "191393" in host.events,
        "activatedGoldenParrot": root.value("activatedGoldenParrot") == "true"
        if root.value("activatedGoldenParrot") is not None
        else None,
        "hostDesertUnlocked": "ccVault" in host.mail,
        "anyCcComplete": any("191393" in p.events for p in state.players),
        "hostCommunityCenterComplete": completed_areas
        and "ccBulletin" in host.mail
        and "JojaMember" not in host.mail,
        "hostJojaMartComplete": joja_areas
        and (
            "JojaMember" in host.mail
            or any("joja" + area in host.mail for area in cc_areas)
        ),
        "townKeyHolders": tuple(
            p.player_id for p in state.players if "HasTownKey" in p.mail
        ),
        "anyDesertUnlocked": any("ccVault" in p.mail for p in state.players),
        "gotCapsule": "Got_Capsule" in host.mail,
        "raccoonTreeFallen": "raccoonTreeFallen" in host.mail,
        "sawQiPlane": "sawQiPlane" in host.mail,
        "gotFirstBillboardPrizeTicketAny": any(
            "gotFirstBillboardPrizeTicket" in p.mail for p in state.players
        ),
        "hasMatureFairyRoseTonight": None,
        "anyOnlineFarmerHasMonsterMusk": None,
        "theaterDayFirstEntered": _saved_int(theater.snapshot, "dayFirstEntered")
        if theater
        else None,
        "theaterBuilt": "ccMovieTheater" in mail or "ccMovieTheaterJoja" in mail,
        "weatherOverrides": weather,
        "weddingDays": (day,)
        if day is not None and root.value("weddingToday") == "true"
        else (),
        "pendingNightEvents": tuple(p for p in priority if p in pending),
        "goldenCoconutCracked": state.world.golden_coconut_cracked,
        "divorcedNpcs": [
            tuple(n for n, f in p.friendship_facts.items() if f.status == "Divorced")
            for p in state.players
        ],
        "equippedMakeoverItems": [
            tuple(
                (kind, i.item_id, i.name)
                for kind in ("hat", "shirtItem")
                for i in p.equipment.get(kind, ())
            )
            for p in state.players
        ],
        "makeoverOutfits": data.catalogs.get("game_MakeoverOutfits"),
    }


def _context_save(
    state: GameState, data: GameData, options: ReportPredictionOptions
) -> MappingProxyType[str, Any]:
    player, metadata = state.player, state.metadata
    version = state.rules_version
    mail = player.mail
    values = {
        **_world_inputs(state, data),
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
        "mp_ids": [p.player_id for p in state.players],
        "playerLuck": [
            player_values(state, options, index)["dailyLuck"]
            for index in range(len(state.players))
        ],
        "gender": [
            p.gender or ("Male" if p.is_male else "Female") for p in state.players
        ],
        "deepestMineLevel": player.deepest_mine_level or 0,
        "timesFedRaccoons": state.world.times_fed_raccoons or 0,
        "raccoonBundleSeason": _saved_int(
            state.snapshot, "seasonOfCurrentRaccoonBundle"
        ),
        "raccoonBundleComplete": tuple(
            node.text() == "true"
            for node in state.snapshot.findall("raccoonBundles/boolean")
        ),
        "raccoonLastCompletedDay": _saved_int(
            state.snapshot, "daysPlayedWhenLastRaccoonBundleWasFinished"
        ),
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
        values["dailyLuck"] += f32(0.025)
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
        values[name] = data.catalogs["predictor_" + catalog]
    values["donatedItems"] = dict(values["donatedItems"])
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
            player.friendship_facts.get("Krobus") is None
            or player.friendship_facts["Krobus"].status == "Unmet"
        ):
            continue
        values["characters"].append(name)
    for location in state.world.locations:
        for item_id in location.museum_items:
            entry = values["objects"].get("_" + item_id)
            if entry:
                values["donatedItems"][entry["name"]] = 1
    if rules.compare_version(version, "1.6") >= 0:
        values["geodeContents"] = dict(values["geodeContents"])
        values["geodeContents"]["275"] = (
            *values["geodeContents"]["275"],
            "_Book_Artifact",
        )
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
    if prices:
        values["objects"] = dict(values["objects"])
    for item_id, price in prices.items():
        values["objects"][item_id] = {**values["objects"][item_id], "price": price}
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
    return MappingProxyType(
        {
            key: value if isinstance(value, MappingProxyType) else freeze(value)
            for key, value in values.items()
        }
    )


def player_values(
    state: GameState, options: ReportPredictionOptions, index: int
) -> dict[str, Any]:
    player = state.players[index]
    charm = "HasSpecialCharm" in player.mail or player.has_special_charm is True
    return {
        "goldenCoconutCracked": state.world.golden_coconut_cracked,
        "hasArtifactFound": "artifactFound" in player.mail | _pending_mail(player),
        "hasGoldenCoconutHat": "goldenCoconutHat"
        in player.mail | _pending_mail(player),
        "fishingLevel": player.skills.get("fishing"),
        "hasFarmingMastery": player.stats.get("mastery_0", 0) > 0,
        "houseUpgradeLevel": player.house_upgrade_level,
        "enchantmentTools": saved_enchantment_tools(player),
        "timesReachedMineBottom": player.stats.get("timesReachedMineBottom", 0),
        "hasQuartzGlobeRecipe": "Quartz Globe"
        in player.collections.get("craftingRecipes", {}),
        "deepestMineLevel": player.deepest_mine_level or 0,
        "quarryUnlocked": "ccCraftsRoom" in player.mail,
        "desertUnlocked": "ccVault" in player.mail,
        "greenhouseUnlocked": "ccPantry" in player.mail,
        "theaterUnlocked": "ccMovieTheater" in player.mail
        and "ccMovieTheaterJoja" not in player.mail,
        "ccComplete": "191393" in player.events,
        "jojaComplete": "502261" in player.events,
        "hasSpecialCharm": charm,
        "gotMysteryBook": "GotMysteryBook" in player.mail,
        "hasGarbageBook": player.stats.get("Book_Trash", 0) > 0,
        "hasFurnaceRecipe": "Furnace" in player.collections.get("craftingRecipes", {}),
        "dailyLuck": (options.daily_luck if options.daily_luck is not None else -0.1)
        + (f32(0.025) if charm else 0),
    }
