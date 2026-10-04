"""Native calendar and world event prediction rules (MouseyPounds, MIT; predictor b9e7c71)."""

from .report_support import (
    floor,
    fmod,
    SystemRandom,
    random_seed,
    hash_string,
    int32,
    trunc_div,
    trunc_rem,
    deepcopy,
    ordered_keys,
    set_slot,
    remove_slice,
    invalid_number,
    exact_seed_part,
    compare_version,
    capture,
)


def predict_mines(context, is_search=None, offset=None):
    """Predict independent days, preserving every per-floor random draw."""
    save = context.save
    before_14 = compare_version(save["version"], "1.4") < 0
    before_15 = compare_version(save["version"], "1.5") < 0
    before_16 = compare_version(save["version"], "1.6") < 0
    if context.day_range is not None:
        days = range(*context.day_range)
    else:
        if offset is None:
            offset = 28 * floor(save["daysPlayed"] / 28)
        days = range(offset + 1, offset + 29)
    for day in days:
        rainbow_lights = []
        infested_monster = []
        infested_slime = []
        quarry_level = []
        dino_level = []
        if before_14:
            mine_level = 1
            while mine_level < 120:
                if fmod(mine_level, 5) == 0:
                    mine_level += 1
                    continue
                rng = SystemRandom(
                    day + save.get("dayAdjust") + mine_level + save.get("gameID") / 2
                )
                if (fmod(mine_level, 40) > 5 and fmod(mine_level, 40) < 30) and fmod(
                    mine_level, 40
                ) != 19:
                    if rng.double() < 0.044:
                        if rng.double() < 0.5:
                            infested_monster.append(mine_level)
                        else:
                            infested_slime.append(mine_level)
                        mine_level += 1
                        continue
                rng = SystemRandom(
                    day + save.get("dayAdjust") + mine_level + save.get("gameID") / 2
                )
                if rng.double() < 0.3 and mine_level > 2:
                    rng.double()
                rng.double()
                if rng.double() < 0.035 and mine_level > 80:
                    rainbow_lights.append(mine_level)
                mine_level += 1
        else:
            mine_level = 1
            while mine_level < 120:
                skip_mushroom_check = False
                if fmod(mine_level, 5) == 0:
                    mine_level += 1
                    continue
                if before_16:
                    rng = SystemRandom(
                        day
                        + save.get("dayAdjust")
                        + mine_level * 100
                        + save.get("gameID") / 2
                    )
                else:
                    rng = SystemRandom(
                        random_seed(
                            day + save.get("dayAdjust"),
                            save.get("gameID") / 2,
                            mine_level * 100,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                if (
                    (rng.double() < 0.044 and fmod(mine_level, 40) > 5)
                    and fmod(mine_level, 40) < 30
                ) and fmod(mine_level, 40) != 19:
                    if rng.double() < 0.5:
                        infested_monster.append(mine_level)
                    else:
                        infested_slime.append(mine_level)
                    skip_mushroom_check = True
                elif (rng.double() < 0.044 and save.get("quarryUnlocked")) and fmod(
                    mine_level, 40
                ) > 1:
                    if rng.double() < 0.25 and before_15:
                        quarry_level.append(f"{mine_level}*")
                    else:
                        quarry_level.append(mine_level)
                    skip_mushroom_check = True
                if skip_mushroom_check:
                    mine_level += 1
                    continue
                if before_16:
                    rng = SystemRandom(
                        (day + save.get("dayAdjust")) * mine_level
                        + 4 * mine_level
                        + save.get("gameID") / 2
                    )
                else:
                    rng = SystemRandom(
                        random_seed(
                            day + save.get("dayAdjust"),
                            save.get("gameID") / 2,
                            day + save.get("dayAdjust"),
                            mine_level,
                            4 * mine_level,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                if not save.get("hardmodeMines"):
                    if rng.double() < 0.3 and mine_level > 2:
                        rng.double()
                rng.double()
                if rng.double() < 0.035 and mine_level > 80:
                    rainbow_lights.append(mine_level)
                mine_level += 1
            mine_level = 127
            while mine_level < 621:
                if before_16:
                    rng = SystemRandom(
                        day
                        + save.get("dayAdjust")
                        + mine_level * 100
                        + save.get("gameID") / 2
                    )
                else:
                    rng = SystemRandom(
                        random_seed(
                            day + save.get("dayAdjust"),
                            save.get("gameID") / 2,
                            mine_level * 100,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                if rng.double() < 0.044:
                    not rng.double() < 0.5
                    if rng.double() < 0.5:
                        dino_level.append(mine_level - 120)
                mine_level += 1
        capture(
            context,
            "predictMines",
            {
                "day": day,
                "rainbowLights": rainbow_lights,
                "infestedMonster": infested_monster,
                "infestedSlime": infested_slime,
                "quarryLevel": quarry_level,
                "dinoLevel": dino_level,
            },
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
    if save.get("deepestMineLevel") > 40:
        possible_items.extend(
            ["Aquamarine", "Jade", "Diamond", "Frozen Tear", "Purple Mushroom"]
        )
    if save.get("deepestMineLevel") > 80:
        possible_items.extend(["Ruby", "Emerald", "Fire Quartz"])
    if save.get("desertUnlocked"):
        possible_items.extend(["Coconut", "Cactus Fruit", "Sandfish", "Scorpion Carp"])
    if save.get("hasFurnaceRecipe"):
        possible_items.extend(["Copper Bar", "Iron Bar", "Gold Bar", "Refined Quartz"])
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
        case 0 | 1:
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
        case 0 | 1 | 2:
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
        case 0 | 1 | 2 | 3:
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
        week,
        week_day,
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
    luck_check = 0.2 + save.get("dailyLuck")
    can_i_d = [
        "JodiAndKent",
        "EmilyAndHaley",
        "Mayor",
        "Museum",
        "Blacksmith",
        "Saloon",
        "Evelyn",
        "JojaMart",
    ]
    tile_x = [13, 19, 56, 108, 97, 47, 52, 110]
    tile_y = [86, 89, 85, 91, 80, 70, 63, 56]
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
    if compare_version(save.get("version"), "1.6") >= 0 and save.get("hasGarbageBook"):
        luck_check = luck_check + 0.2
    week = 0
    while week < 4:
        week_day = 1
        while week_day < 8:
            day = 7 * week + week_day + offset
            which_can = 0
            while which_can < 8:
                if compare_version(save.get("version"), "1.6") >= 0:
                    seed = random_seed(
                        day + save.get("dayAdjust"),
                        save.get("gameID") / 2,
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
                if compare_version(save.get("version"), "1.6") >= 0:
                    mega = False
                    double_mega = False
                    base_chance_passed = rng.double() < luck_check
                    if save.get("trashCansChecked")[0] >= 20 and rng.double() < 0.002:
                        double_mega = True
                        trash_item = "Garbage Hat"
                    elif save.get("trashCansChecked")[0] >= 50 and rng.double() < 0.002:
                        double_mega = True
                        trash_item = "Trash Catalogue"
                    if trash_item == "":
                        if save.get("qiCropsActive") and rng.double() < 0.25:
                            trash_item = "Qi Bean"
                        elif base_chance_passed:
                            match which_can:
                                case 4:
                                    if rng.double() < 0.2 + save.get("dailyLuck"):
                                        match rng.next(3):
                                            case 0:
                                                trash_item = "Copper Ore"
                                            case 0 | 1:
                                                trash_item = "Iron Ore"
                                            case 0 | 1 | 2:
                                                trash_item = "Coal"
                                        stack = rng.next(1, 5)
                                        if stack > 1:
                                            trash_item = f"{trash_item} x{stack}"
                                case 4 | 6:
                                    if rng.double() < 0.2 + save.get("dailyLuck"):
                                        trash_item = "Cookie"
                                case 4 | 6 | 7:
                                    rng_synced = SystemRandom(
                                        random_seed(
                                            hash_string("garbage_joja"),
                                            save.get("gameID"),
                                            day + save.get("dayAdjust"),
                                            legacy=save["useLegacyRandom"],
                                        )
                                    )
                                    if rng_synced.double() < 0.2:
                                        if save.get("theaterUnlocked"):
                                            if rng.next(4) > 0:
                                                trash_item = "Corn"
                                            else:
                                                trash_item = "Movie Ticket"
                                        elif not save.get("ccComplete"):
                                            trash_item = "Joja Cola"
                                case 4 | 6 | 7 | 3:
                                    rng_synced = SystemRandom(
                                        random_seed(
                                            hash_string("garbage_museum_535"),
                                            save.get("gameID"),
                                            day + save.get("dayAdjust"),
                                            legacy=save["useLegacyRandom"],
                                        )
                                    )
                                    if rng_synced.double() < 0.2 + save.get(
                                        "dailyLuck"
                                    ):
                                        rng_synced = SystemRandom(
                                            random_seed(
                                                hash_string("garbage_museum_749"),
                                                save.get("gameID"),
                                                day + save.get("dayAdjust"),
                                                legacy=save["useLegacyRandom"],
                                            )
                                        )
                                        if rng_synced.double() < 0.05:
                                            trash_item = "Omni Geode"
                                        else:
                                            trash_item = "Geode"
                                case 4 | 6 | 7 | 3 | 5:
                                    rng_synced = SystemRandom(
                                        random_seed(
                                            hash_string("garbage_saloon_dish"),
                                            save.get("gameID"),
                                            day + save.get("dayAdjust"),
                                            legacy=save["useLegacyRandom"],
                                        )
                                    )
                                    if rng_synced.double() < 0.2 + save.get(
                                        "dailyLuck"
                                    ):
                                        trash_item = "Dish of the Day"
                    if trash_item == "":
                        mega = (
                            save.get("trashCansChecked")[0] >= 20
                            and rng.double() < 0.01
                        )
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
                        if save.get("trashCansChecked")[0] >= 20
                        and rng.double() < 0.002
                        else False
                    )
                    if double_mega:
                        trash_item = "Garbage Hat"
                    elif mega or rng.double() < luck_check:
                        match rng.next(10):
                            case 0:
                                trash_item = "Trash (item)"
                            case 0 | 1:
                                trash_item = "Joja Cola"
                            case 0 | 1 | 2:
                                trash_item = "Broken Glasses"
                            case 0 | 1 | 2 | 3:
                                trash_item = "Broken CD"
                            case 0 | 1 | 2 | 3 | 4:
                                trash_item = "Soggy Newspaper"
                            case 0 | 1 | 2 | 3 | 4 | 5:
                                trash_item = "Bread"
                            case 0 | 1 | 2 | 3 | 4 | 5 | 6:
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
                            case 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7:
                                trash_item = "Field Snack"
                            case 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8:
                                match rng.next(3):
                                    case 0:
                                        trash_item = "Acorn"
                                    case 0 | 1:
                                        trash_item = "Maple Seed"
                                    case 0 | 1 | 2:
                                        trash_item = "Pine Cone"
                            case 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9:
                                trash_item = "Green Algae"
                        if which_can == 3 and rng.double() < luck_check:
                            trash_item = "Geode"
                            if rng.double() < 0.05:
                                trash_item = "Omni Geode"
                        if which_can == 4 and rng.double() < luck_check:
                            match rng.next(3):
                                case 0:
                                    trash_item = "Copper Ore"
                                case 0 | 1:
                                    trash_item = "Iron Ore"
                                case 0 | 1 | 2:
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
                            "tileX": tile_x,
                            "tileY": tile_y,
                        },
                    )
                which_can += 1
            week_day += 1
        week += 1
    return None


def predict_trains(context, is_search=None, offset=None):
    save = context.save
    ampm, day, hour, min, rng, this_train, train_time, week, week_day = (
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
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    week = 0
    while week < 4:
        week_day = 1
        while week_day < 8:
            day = 7 * week + week_day + offset
            if compare_version(save.get("version"), "1.6") >= 0:
                rng = SystemRandom(
                    random_seed(
                        day + save.get("dayAdjust"),
                        save.get("gameID") / 2,
                        legacy=save["useLegacyRandom"],
                    )
                )
            else:
                rng = SystemRandom(save.get("gameID") / 2 + day + save.get("dayAdjust"))
            if day < 31:
                this_train = "Railroad not yet accessible"
            else:
                this_train = "\xa0 (No train) \xa0"
                if rng.double() < 0.2:
                    train_time = rng.next(900, 1800)
                    train_time = train_time - fmod(train_time, 10)
                    hour = floor(train_time / 100)
                    min = fmod(train_time, 100)
                    if min < 60:
                        if hour > 12:
                            hour = hour - 12
                            ampm = " pm"
                        elif hour == 12:
                            ampm = " pm"
                        else:
                            ampm = " am"
                        if min == 0:
                            min = "00"
                        this_train = f" Train at {hour}:{min}{ampm}"
            capture(
                context,
                "predictTrains",
                {"day": day, "thisTrain": this_train, "trainTime": train_time},
            )
            week_day += 1
        week += 1
    return None


def predict_night(context, is_search=None, offset=None):
    save = context.save
    (
        could_be_windstorm,
        day,
        i,
        month,
        next_roll,
        rng,
        this_event,
        week,
        week_day,
        year,
    ) = (None, None, None, None, None, None, None, None, None, None)
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    month = floor(offset / 28)
    year = 1 + floor(offset / 112)
    week = 0
    while week < 4:
        week_day = 1
        while week_day < 8:
            day = 7 * week + week_day + offset
            could_be_windstorm = False
            if day + save.get("dayAdjust") == 30:
                this_event = " Earthquake"
            elif compare_version(save.get("version"), "1.6") >= 0:
                rng = SystemRandom(
                    random_seed(
                        day + 1 + save.get("dayAdjust"),
                        save.get("gameID") / 2,
                        legacy=save["useLegacyRandom"],
                    )
                )
                i = 0
                while i < 10:
                    rng.double()
                    i += 1
                if save.get("greenhouseUnlocked"):
                    could_be_windstorm = rng.double() < 0.1
                next_roll = rng.double()
                if not save.get("greenhouseUnlocked"):
                    could_be_windstorm = next_roll < 0.1
                if next_roll < 0.01 and fmod(month, 4) < 3:
                    this_event = " Fairy"
                elif rng.double() < 0.01 and day + 1 + save.get("dayAdjust") > 20:
                    this_event = " Witch"
                elif rng.double() < 0.01 and day + 1 + save.get("dayAdjust") > 5:
                    this_event = " Meteor"
                elif rng.double() < 0.005:
                    this_event = " Stone Owl"
                elif rng.double() < 0.008 and year > 1:
                    this_event = " Strange Capsule"
                else:
                    this_event = "\xa0 (No event) \xa0"
            else:
                rng = SystemRandom(
                    save.get("gameID") / 2 + day + 1 + save.get("dayAdjust")
                )
                if (
                    compare_version(save.get("version"), "1.3") < 0
                    and save.get("canHaveChildren")
                ) and rng.double() < 0.05:
                    this_event = ' "Want a Baby?"'
                elif rng.double() < 0.01 and fmod(month, 4) < 3:
                    this_event = " Fairy"
                elif rng.double() < 0.01:
                    this_event = " Witch"
                elif rng.double() < 0.01:
                    this_event = " Meteor"
                elif compare_version(save.get("version"), "1.5") < 0:
                    if rng.double() < 0.01 and year > 1:
                        this_event = " Strange Capsule"
                    elif rng.double() < 0.01:
                        this_event = " Stone Owl"
                    else:
                        this_event = "\xa0 (No event) \xa0"
                elif compare_version(save.get("version"), "1.5.3") < 0:
                    if rng.double() < 0.008 and year > 1:
                        this_event = " Strange Capsule"
                    elif rng.double() < 0.008:
                        this_event = " Stone Owl"
                    else:
                        this_event = "\xa0 (No event) \xa0"
                elif rng.double() < 0.005:
                    this_event = " Stone Owl"
                elif rng.double() < 0.008 and year > 1:
                    this_event = " Strange Capsule"
                else:
                    this_event = "\xa0 (No event) \xa0"
            capture(
                context,
                "predictNight",
                {
                    "day": day,
                    "thisEvent": this_event,
                    "couldBeWindstorm": could_be_windstorm,
                },
            )
            week_day += 1
        week += 1
    return None


def predict_crane(context, is_search=None, offset=None):
    save = context.save
    day, rng, this_event, week, week_day = (None, None, None, None, None)
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    week = 0
    while week < 4:
        week_day = 1
        while week_day < 8:
            day = 7 * week + week_day + offset
            if compare_version(save.get("version"), "1.6") >= 0:
                rng = SystemRandom(
                    random_seed(
                        save.get("gameID"),
                        day + save.get("dayAdjust") - 1,
                        legacy=save["useLegacyRandom"],
                    )
                )
            else:
                rng = SystemRandom(save.get("gameID") + day + save.get("dayAdjust") - 1)
            if compare_version(save.get("version"), "1.4") >= 0 and rng.double() < 0.25:
                this_event = " (Game In Use)"
            else:
                this_event = "Game Can Be Played \xa0"
            capture(context, "predictCrane", {"day": day, "thisEvent": this_event})
            week_day += 1
        week += 1
    return None


def predict_green_rain(context, is_search=None, offset=None):
    save = context.save
    (
        day,
        day_of_month,
        festival_days,
        gr_days,
        green_rain_day,
        month,
        rain_chance,
        rng,
        season,
        weather_town,
        week,
        week_day,
        year,
    ) = (None, None, None, None, None, None, None, None, None, None, None, None, None)
    gr_days = [5, 6, 7, 14, 15, 16, 18, 23]
    festival_days = deepcopy(context.catalogs["predictor_festival_days"])
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    month = floor(offset / 28)
    season = fmod(month, 4)
    year = 1 + floor(offset / 112)
    rng = SystemRandom(
        random_seed(year * 777, save.get("gameID"), legacy=save["useLegacyRandom"])
    )
    green_rain_day = gr_days[int(rng.next(len(gr_days)))]
    week = 0
    while week < 4:
        week_day = 1
        while week_day < 8:
            day = 7 * week + week_day + offset
            weather_town = "Sun"
            if ((day == 1 or day == 2) or day == 4) or fmod(day, 28) == 1:
                weather_town = "Sun"
            elif day == 3:
                weather_town = "Rain"
            elif str(fmod(day, 112)) in festival_days:
                weather_town = festival_days[str(fmod(day, 112))]
            else:
                match season:
                    case 0 | 2:
                        rng = SystemRandom(
                            random_seed(
                                hash_string("location_weather"),
                                save.get("gameID"),
                                day - 1,
                                legacy=save["useLegacyRandom"],
                            )
                        )
                        if rng.double() < 0.183:
                            weather_town = "Rain"
                    case 0 | 2 | 1:
                        day_of_month = fmod(day, 112) - 28
                        rng = SystemRandom(
                            random_seed(
                                day - 1,
                                save.get("gameID") / 2,
                                hash_string("summer_rain_chance"),
                                legacy=save["useLegacyRandom"],
                            )
                        )
                        if day_of_month == green_rain_day:
                            weather_town = "Green Rain"
                        elif fmod(day_of_month, 13) == 0:
                            weather_town = "Storm"
                        else:
                            rain_chance = 0.12 + 0.003 * (day_of_month - 1)
                            if rng.double() < rain_chance:
                                weather_town = "Rain"
            capture(
                context,
                "predictGreenRain",
                {
                    "day": day,
                    "weatherTown": weather_town,
                    "greenRainDay": green_rain_day,
                    "season": season,
                },
            )
            week_day += 1
        week += 1
    return None


def predict_statues(context, is_search=None, offset=None):
    save = context.save
    (
        bless_no_rain,
        bless_rain,
        blessing_names,
        coords,
        day,
        dwarf1,
        dwarf2,
        dwarf_names,
        i,
        index,
        j,
        map_dim,
        pb_maps,
        player,
        rng,
        roll,
        shard,
        week,
        week_day,
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
    )
    blessing_names = [
        "Speed",
        "Luck",
        "Energy",
        "Waters",
        "Friendship",
        "Fangs",
        "Butterfly",
    ]
    dwarf_names = ["+1 Ore", "Ladders", "Coal", "Bomb Immunity", "Geodes"]
    pb_maps = [
        "Forest",
        "Town",
        "Beach",
        "Mountain",
        "Secret Woods",
        "Bus Stop",
        "Backwoods",
    ]
    map_dim = [
        [120, 120],
        [130, 110],
        [104, 50],
        [135, 41],
        [60, 32],
        [65, 30],
        [50, 40],
    ]
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    week = 0
    while week < 4:
        week_day = 1
        while week_day < 8:
            day = 7 * week + week_day + offset
            rng = SystemRandom(
                random_seed(
                    day,
                    save.get("gameID") / 2,
                    day * 777,
                    legacy=save["useLegacyRandom"],
                )
            )
            j = 0
            while j < 8:
                rng.next()
                j += 1
            roll = rng.double()
            bless_rain = floor(roll * 6)
            bless_no_rain = floor(roll * 7)
            if bless_no_rain == 6:
                if "mp_ids" in save:
                    player = 0
                    while player < len(save.get("mp_ids")):
                        rng = SystemRandom(
                            random_seed(
                                exact_seed_part(int(day)),
                                exact_seed_part(trunc_div(int(save.get("gameID")), 2)),
                                exact_seed_part(
                                    trunc_rem(save.get("mp_ids")[int(player)], 10000)
                                ),
                                legacy=save["useLegacyRandom"],
                            )
                        )
                        shard = rng.double() < 0.05 + save.get("dailyLuck")
                        rng = SystemRandom(
                            random_seed(
                                exact_seed_part(int(day)),
                                exact_seed_part(trunc_div(int(save.get("gameID")), 2)),
                                exact_seed_part(
                                    trunc_rem(save.get("mp_ids")[int(player)], 10000)
                                ),
                                legacy=save["useLegacyRandom"],
                            )
                        )
                        index = rng.next(len(pb_maps))
                        coords = []
                        i = 0
                        while i <= 32:
                            coords.append(
                                {
                                    "x": rng.next(map_dim[int(index)][0]),
                                    "y": rng.next(map_dim[int(index)][1]),
                                }
                            )
                            i += 1
                        capture(
                            context,
                            "predictStatues",
                            {
                                "day": day,
                                "player": player,
                                "index": index,
                                "shard": shard,
                                "pbMaps": pb_maps,
                                "coords": coords,
                            },
                        )
                        player += 1
            rng = SystemRandom(
                random_seed(
                    day * 77, save.get("gameID"), legacy=save["useLegacyRandom"]
                )
            )
            dwarf1 = rng.next(5)
            dwarf2 = dwarf1
            while dwarf2 == dwarf1:
                dwarf2 = rng.next(5)
            capture(
                context,
                "predictStatues",
                {
                    "day": day,
                    "blessRain": bless_rain,
                    "blessNoRain": bless_no_rain,
                    "dwarf1": dwarf1,
                    "dwarf2": dwarf2,
                    "blessingNames": blessing_names,
                    "dwarfNames": dwarf_names,
                },
            )
            week_day += 1
        week += 1
    return None
