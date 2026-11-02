"""Trash rules adapted from MouseyPounds (MIT; b9e7c71)."""

from stardew.domain.numeric import f32

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    fmod,
    hash_string,
    prediction_days,
    random_seed,
    trunc_div,
)


def get_random_item_from_season(context, rng=None, season=None):
    save = context.save
    (possible_items,) = (None,)
    possible_items = [
        "Topaz",
        "Amethyst",
        "Cave Carrot",
        "Quartz",
        "Earth Crystal",
        "Seaweed",
        "Joja Cola",
        "Green Algae",
        "Red Mushroom",
    ]
    reached_bottom = (save.get("timesReachedMineBottom") or 0) >= 1
    if save.get("deepestMineLevel") > 40 or reached_bottom:
        possible_items.extend(
            ["Aquamarine", "Jade", "Diamond", "Frozen Tear", "Purple Mushroom"]
        )
    if save.get("deepestMineLevel") > 80 or reached_bottom:
        possible_items.extend(["Ruby", "Emerald", "Fire Quartz"])
    if save.get("anyDesertUnlocked", save.get("desertUnlocked")):
        possible_items.extend(["Coconut", "Cactus Fruit", "Sandfish", "Scorpion Carp"])
    if save.get("hasFurnaceRecipe"):
        possible_items.extend(["Copper Bar", "Iron Bar", "Gold Bar", "Refined Quartz"])
    if save.get("hasQuartzGlobeRecipe"):
        possible_items.append("Quartz Globe")
    match season:
        case 0:
            possible_items.extend(
                [
                    "Wild Horseradish",
                    "Daffodil",
                    "Leek",
                    "Dandelion",
                    "Anchovy",
                    "Sardine",
                    "Bream",
                    "Largemouth Bass",
                    "Smallmouth Bass",
                    "Carp",
                    "Catfish",
                    "Sunfish",
                    "Herring",
                    "Eel",
                    "Seaweed",
                    "Joja Cola",
                    "Flounder",
                ]
            )
        case 1:
            possible_items.extend(
                [
                    "Pufferfish",
                    "Tuna",
                    "Bream",
                    "Largemouth Bass",
                    "Rainbow Trout",
                    "Carp",
                    "Pike",
                    "Sunfish",
                    "Red Mullet",
                    "Octopus",
                    "Red Snapper",
                    "Super Cucumber",
                    "Spice Berry",
                    "Grape",
                    "Sweet Pea",
                    "Flounder",
                ]
            )
        case 2:
            possible_items.extend(
                [
                    "Common Mushroom",
                    "Wild Plum",
                    "Hazelnut",
                    "Blackberry",
                    "Anchovy",
                    "Sardine",
                    "Bream",
                    "Largemouth Bass",
                    "Smallmouth Bass",
                    "Salmon",
                    "Walleye",
                    "Carp",
                    "Catfish",
                    "Eel",
                    "Red Snapper",
                    "Sea Cucumber",
                    "Super Cucumber",
                    "Midnight Carp",
                ]
            )
        case 3:
            possible_items.extend(
                [
                    "Winter Root",
                    "Crystal Fruit",
                    "Snow Yam",
                    "Crocus",
                    "Tuna",
                    "Sardine",
                    "Bream",
                    "Largemouth Bass",
                    "Walleye",
                    "Perch",
                    "Pike",
                    "Red Mullet",
                    "Herring",
                    "Red Snapper",
                    "Squid",
                    "Sea Cucumber",
                    "Midnight Carp",
                ]
            )
    return possible_items[int(rng.next(len(possible_items)))]


def predict_trash(context, is_search=None, offset=None):
    save = context.save
    (
        base_chance_passed,
        can_i_d,
        day,
        double_mega,
        fallback_list,
        i,
        luck_check,
        mega,
        month,
        prewarm,
        rng,
        rng_season,
        rng_synced,
        roll,
        seed,
        stack,
        tile_x,
        tile_y,
        trash_item,
        _week,
        _week_day,
        which_can,
    ) = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )
    modern = compare_version(save["version"], "1.6") >= 0
    special_chance = (
        f32(f32(0.2) + f32(save["dailyLuck"])) if modern else 0.2 + save["dailyLuck"]
    )
    luck_check = special_chance
    can_i_d = [
        "JodiAndKent",
        "EmilyAndHaley",
        "Mayor",
        "Museum",
        "Blacksmith",
        "Saloon",
        "Evelyn",
        "JojaMart",
        "DesertFestival",
    ]
    tile_x = [13, 19, 56, 108, 97, 47, 52, 110, None]
    tile_y = [86, 89, 85, 91, 80, 70, 63, 56, None]
    fallback_list = [
        "_153",
        "_216",
        "_403",
        "_309",
        "_310",
        "_311",
        "SEASON",
        "_168",
        "_167",
        "_170",
        "_171",
        "_172",
    ]
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    month = floor(offset / 28)
    if modern and save.get("hasGarbageBook"):
        luck_check = f32(luck_check + f32(0.2))
    for day in prediction_days(context, offset):
        game_day = day + save["dayAdjust"]
        festival_can = (
            modern
            and (game_day - 1) % 112 + 1 in (15, 16, 17)
            and save.get("hostDesertUnlocked")
        )
        number_of_cans = 9 if festival_can else 8
        which_can = 0
        while which_can < number_of_cans:
            if compare_version(save.get("version"), "1.6") >= 0:
                seed = random_seed(
                    day + save.get("dayAdjust"),
                    trunc_div(save["gameID"], 2),
                    777 + hash_string(can_i_d[int(which_can)]),
                    legacy=save["useLegacyRandom"],
                )
            else:
                seed = (
                    save.get("gameID") / 2
                    + day
                    + save.get("dayAdjust")
                    + 777
                    + which_can * 77
                )
            rng = SystemRandom(seed)
            prewarm = rng.next(0, 100)
            i = 0
            while i < prewarm:
                rng.double()
                i += 1
            prewarm = rng.next(0, 100)
            i = 0
            while i < prewarm:
                rng.double()
                i += 1
            trash_item = ""
            stack = 1
            if compare_version(save.get("version"), "1.6") >= 0:
                mega = False
                double_mega = False
                base_chance_passed = rng.double() < luck_check
                if save.get("trashCansChecked")[
                    context.player_index
                ] >= 20 and rng.double() < f32(0.002):
                    double_mega = True
                    trash_item = "Garbage Hat"
                elif save.get("trashCansChecked")[
                    context.player_index
                ] >= 50 and rng.double() < f32(0.002):
                    double_mega = True
                    trash_item = "Trash Catalogue"
                if trash_item == "":
                    if (
                        base_chance_passed
                        and save.get("qiCropsActive")
                        and rng.double() < 0.25
                    ):
                        trash_item = "Qi Bean"
                    elif which_can == 8:
                        # The festival entry ignores base chance, but remains
                        # after the shared BeforeAll items in the game table.
                        trash_item = "Calico Egg"
                        stack = rng.next(5, 9)
                    elif base_chance_passed:
                        match which_can:
                            case 4:
                                if rng.double() < special_chance:
                                    match rng.next(3):
                                        case 0:
                                            trash_item = "Copper Ore"
                                        case 1:
                                            trash_item = "Iron Ore"
                                        case 2:
                                            trash_item = "Coal"
                                    stack = rng.next(1, 5)
                                    if stack > 1:
                                        trash_item = f"{trash_item} x{stack}"
                            case 6:
                                if rng.double() < special_chance:
                                    trash_item = "Cookie"
                            case 7:
                                rng_synced = SystemRandom(
                                    random_seed(
                                        hash_string("garbage_joja"),
                                        save.get("gameID"),
                                        day + save.get("dayAdjust"),
                                        legacy=save["useLegacyRandom"],
                                    )
                                )
                                if rng_synced.double() < f32(0.2):
                                    if save.get(
                                        "hostTheaterUnlocked",
                                        save.get("theaterUnlocked"),
                                    ):
                                        if rng.next(4) > 0:
                                            trash_item = "Corn"
                                        else:
                                            trash_item = "Movie Ticket"
                                    elif not save.get(
                                        "anyCcComplete", save.get("ccComplete")
                                    ):
                                        trash_item = "Joja Cola"
                            case 3:
                                rng_synced = SystemRandom(
                                    random_seed(
                                        hash_string("garbage_museum_535"),
                                        save.get("gameID"),
                                        day + save.get("dayAdjust"),
                                        legacy=save["useLegacyRandom"],
                                    )
                                )
                                if rng_synced.double() < special_chance:
                                    rng_synced = SystemRandom(
                                        random_seed(
                                            hash_string("garbage_museum_749"),
                                            save.get("gameID"),
                                            day + save.get("dayAdjust"),
                                            legacy=save["useLegacyRandom"],
                                        )
                                    )
                                    if rng_synced.double() < f32(0.05):
                                        trash_item = "Omni Geode"
                                    else:
                                        trash_item = "Geode"
                            case 5:
                                rng_synced = SystemRandom(
                                    random_seed(
                                        hash_string("garbage_saloon_dish"),
                                        save.get("gameID"),
                                        day + save.get("dayAdjust"),
                                        legacy=save["useLegacyRandom"],
                                    )
                                )
                                if rng_synced.double() < special_chance:
                                    trash_item = "Dish of the Day"
                if trash_item == "":
                    mega = save.get("trashCansChecked")[
                        context.player_index
                    ] >= 20 and rng.double() < f32(0.01)
                    if mega or base_chance_passed:
                        roll = rng.next(7 if mega else len(fallback_list))
                        if fallback_list[int(roll)] == "SEASON":
                            trash_item = get_random_item_from_season(
                                context, rng, fmod(month, 4)
                            )
                        else:
                            trash_item = (
                                save.get("objects")
                                .get(str(fallback_list[int(roll)]))
                                .get("name")
                            )
            else:
                mega = True if rng.double() < 0.01 else False
                double_mega = (
                    True
                    if save.get("trashCansChecked")[context.player_index] >= 20
                    and rng.double() < 0.002
                    else False
                )
                if double_mega:
                    trash_item = "Garbage Hat"
                elif mega or rng.double() < luck_check:
                    match rng.next(10):
                        case 0:
                            trash_item = "Trash (item)"
                        case 1:
                            trash_item = "Joja Cola"
                        case 2:
                            trash_item = "Broken Glasses"
                        case 3:
                            trash_item = "Broken CD"
                        case 4:
                            trash_item = "Soggy Newspaper"
                        case 5:
                            trash_item = "Bread"
                        case 6:
                            rng_season = SystemRandom(
                                save.get("gameID")
                                + day
                                + save.get("dayAdjust")
                                + tile_x[int(which_can)] * 653
                                + tile_y[int(which_can)] * 777
                            )
                            trash_item = get_random_item_from_season(
                                context, rng_season, fmod(month, 4)
                            )
                        case 7:
                            trash_item = "Field Snack"
                        case 8:
                            match rng.next(3):
                                case 0:
                                    trash_item = "Acorn"
                                case 1:
                                    trash_item = "Maple Seed"
                                case 2:
                                    trash_item = "Pine Cone"
                        case 9:
                            trash_item = "Green Algae"
                    if which_can == 3 and rng.double() < luck_check:
                        trash_item = "Geode"
                        if rng.double() < 0.05:
                            trash_item = "Omni Geode"
                    if which_can == 4 and rng.double() < luck_check:
                        match rng.next(3):
                            case 0:
                                trash_item = "Copper Ore"
                            case 1:
                                trash_item = "Iron Ore"
                            case 2:
                                trash_item = "Coal"
                        rng.next(1, 5)
                    if which_can == 5 and rng.double() < luck_check:
                        trash_item = "Dish of the Day"
                    if which_can == 6 and rng.double() < luck_check:
                        trash_item = "Cookie"
                    if which_can == 7 and rng.double() < 0.2:
                        trash_item = "Joja Cola"
                        if rng.double() < 0.25:
                            trash_item = f"{trash_item} or Movie Ticket"
                        else:
                            trash_item = f"{trash_item} or Corn"
            if trash_item != "":
                capture(
                    context,
                    "predictTrash",
                    {
                        "day": day,
                        "whichCan": which_can,
                        "trashItem": trash_item,
                        "stack": stack,
                        "mega": mega,
                        "doubleMega": double_mega,
                        "tileX": tile_x if which_can == 8 else tile_x[:8],
                        "tileY": tile_y if which_can == 8 else tile_y[:8],
                        "conditions": "First player to search this shared can today; saved counters and progression unchanged before this search",
                    },
                )
            which_can += 1
    return None
