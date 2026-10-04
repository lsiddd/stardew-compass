"""Native festival and save-specific event prediction rules (MouseyPounds, MIT; predictor b9e7c71)."""

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


def predict_mine_chests(context, is_search=None, offset=None):
    save = context.save
    choices, floor, item, rng = (None, None, None, None)
    choices = {
        "10": [
            save.get("boots").get("506"),
            save.get("boots").get("507"),
            save.get("weapons").get("12"),
            save.get("weapons").get("17"),
            save.get("weapons").get("22"),
            save.get("weapons").get("31"),
        ],
        "20": [
            save.get("weapons").get("11"),
            save.get("weapons").get("24"),
            save.get("weapons").get("20"),
            save.get("objects").get("_517").get("name"),
            save.get("objects").get("_519").get("name"),
        ],
        "30": ["(No chest)"],
        "40": [save.get("weapons").get("32")],
        "50": [
            save.get("boots").get("509"),
            save.get("boots").get("510"),
            save.get("boots").get("508"),
            save.get("weapons").get("1"),
            save.get("weapons").get("43"),
        ],
        "60": [
            save.get("weapons").get("21"),
            save.get("weapons").get("44"),
            save.get("weapons").get("6"),
            save.get("weapons").get("18"),
            save.get("weapons").get("27"),
        ],
        "70": [save.get("weapons").get("33")],
        "80": [
            save.get("boots").get("512"),
            save.get("boots").get("511"),
            save.get("weapons").get("10"),
            save.get("weapons").get("7"),
            save.get("weapons").get("46"),
            save.get("weapons").get("19"),
        ],
        "90": [
            save.get("weapons").get("8"),
            save.get("weapons").get("52"),
            save.get("weapons").get("45"),
            save.get("weapons").get("5"),
            save.get("weapons").get("60"),
        ],
        "100": ["Stardrop"],
        "110": [
            save.get("boots").get("514"),
            save.get("boots").get("878"),
            save.get("weapons").get("50"),
            save.get("weapons").get("28"),
        ],
        "120": ["Skull Key"],
    }
    floor = 10
    while floor < 121:
        if compare_version(save.get("version"), "1.6") >= 0:
            rng = SystemRandom(
                random_seed(
                    exact_seed_part(int(save.get("gameID")) * 512),
                    exact_seed_part(int(floor)),
                    legacy=save["useLegacyRandom"],
                )
            )
        else:
            rng = SystemRandom(int32(int(save.get("gameID")) * 512 + floor))
        item = choices.get(str(floor))[int(rng.next(len(choices.get(str(floor)))))]
        if floor != 30:
            item = item
        capture(context, "predictMineChests", {"floor": floor, "item": item})
        floor = floor + 10
    return None


def predict_gem_birds(context, is_search=None, offset=None):
    save = context.save
    birds, gems, i, j, locs, rng, temp = (None, None, None, None, None, None, None)
    birds = ["Green", "Blue", "Red", "Purple", "Brown"]
    gems = {
        "Green": "Emerald",
        "Blue": "Aquamarine",
        "Red": "Ruby",
        "Purple": "Amethyst",
        "Brown": "Topaz",
    }
    locs = [
        "North (Dig Site / Volcano)",
        "South (Docks / Resort)",
        "East (Jungle)",
        "West (Farm)",
    ]
    if compare_version(save.get("version"), "1.6") >= 0:
        rng = SystemRandom(
            random_seed(save.get("gameID"), legacy=save["useLegacyRandom"])
        )
    else:
        rng = SystemRandom(save.get("gameID"))
    i = len(birds)
    while i > 1:
        j = rng.next((i := (i + -1)) - -1)
        temp = birds[int(i)]
        set_slot(birds, i, birds[int(j)])
        set_slot(birds, j, temp)
    i = 0
    while i < len(locs):
        capture(
            context,
            "predictGemBirds",
            {"i": i, "locs": locs, "birds": birds, "gems": gems},
        )
        i += 1
    return None


def predict_winter_star(context, is_search=None, offset=None):
    save = context.save
    (
        UMP_ID,
        base,
        excluded,
        force_old_logic,
        gifts,
        index,
        npcs,
        num_players,
        orig,
        pick,
        player,
        player_name,
        rng,
        secret_santa_get_from,
        secret_santa_give_to,
        seed,
        year,
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
    )
    npcs = deepcopy(context.catalogs["predictor_winter_star_npcs"])
    gift_choices = context.catalogs["predictor_winter_star_gifts"]
    gifts = ""
    excluded = {"Wizard": 1, "Krobus": 1, "Sandy": 1, "Dwarf": 1, "Marlon": 1}
    secret_santa_give_to = ""
    secret_santa_get_from = ""
    num_players = 1
    player_name = "Farmer"
    force_old_logic = False
    if compare_version(save.get("version"), "1.5") >= 0:
        npcs.append("Leo")
        if not save.get("leoMoved"):
            excluded["Leo"] = 1
    if offset is None:
        offset = save.get("year") - 1
    year = offset + 1
    if not save.get("names") is None and (not save.get("mp_ids") is None):
        num_players = len(save.get("names"))
    else:
        force_old_logic = True
    player = 0
    while player < num_players:
        if force_old_logic or compare_version(save.get("version"), "1.3") < 0:
            rng = SystemRandom(save.get("gameID") / 2 - year)
        else:
            UMP_ID = int32(save.get("mp_ids")[int(player)])
            base = int32(trunc_div(int(save.get("gameID")), 2))
            seed = int(int(base) ^ int(year)) ^ int(UMP_ID)
            rng = SystemRandom(seed)
            player_name = save.get("names")[int(player)]
        if not force_old_logic and compare_version(save.get("version"), "1.6") >= 0:
            orig = deepcopy(context.catalogs["predictor_winter_star_original_npcs"])
            if save.get("leoMoved"):
                orig.append("Leo")
            npcs = orig[:]
            secret_santa_give_to = ""
            rng = SystemRandom(
                random_seed(
                    exact_seed_part(trunc_div(int(save.get("gameID")), 2)),
                    exact_seed_part(int(year)),
                    exact_seed_part(save.get("mp_ids")[int(player)]),
                    legacy=save["useLegacyRandom"],
                )
            )
            while secret_santa_give_to == "":
                index = rng.next(len(npcs))
                pick = npcs[int(index)]
                if pick == "Marlon" or (year == 1 and pick == "Kent"):
                    remove_slice(npcs, index, 1)
                else:
                    secret_santa_give_to = pick
            npcs = orig[:]
            secret_santa_get_from = ""
            remove_slice(npcs, npcs.index(secret_santa_give_to), 1)
            rng = SystemRandom(
                random_seed(
                    exact_seed_part(trunc_div(int(save.get("gameID")), 2)),
                    exact_seed_part(int(year)),
                    exact_seed_part(save.get("mp_ids")[int(player)]),
                    legacy=save["useLegacyRandom"],
                )
            )
            while secret_santa_get_from == "":
                index = rng.next(len(npcs))
                pick = npcs[int(index)]
                if pick == "Marlon" or (year == 1 and pick == "Kent"):
                    remove_slice(npcs, index, 1)
                else:
                    secret_santa_get_from = pick
        else:
            secret_santa_give_to = npcs[int(rng.next(len(npcs)))]
            secret_santa_get_from = ""
            while str(secret_santa_give_to) in excluded or (
                year == 1 and secret_santa_give_to == "Kent"
            ):
                secret_santa_give_to = npcs[int(rng.next(len(npcs)))]
            while (
                (
                    secret_santa_get_from == ""
                    or secret_santa_get_from == secret_santa_give_to
                )
                or str(secret_santa_get_from) in excluded
            ) or (year == 1 and secret_santa_get_from == "Kent"):
                secret_santa_get_from = npcs[int(rng.next(len(npcs)))]
        gifts = tuple(
            sorted(gift_choices.get(secret_santa_get_from, gift_choices["DEFAULT"]))
        )
        capture(
            context,
            "predictWinterStar",
            {
                "year": year,
                "player": player,
                "playerName": player_name,
                "secretSantaGiveTo": secret_santa_give_to,
                "secretSantaGetFrom": secret_santa_get_from,
                "gifts": gifts,
            },
        )
        player += 1
    return None


def predict_makeover(context, is_search=None, offset=None):
    save = context.save
    (
        c,
        d,
        day,
        i,
        index,
        k,
        m,
        makeover_choices,
        outfit,
        parts,
        player,
        possible_vendors,
        racer_names,
        racer_pool,
        racers,
        rng,
        roll,
        schedule_exclusion,
        seed,
        umid,
        vendor,
        vendor_pool,
        year,
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
        None,
    )
    makeover_choices = deepcopy(context.catalogs["predictor_makeover_choices"])
    possible_vendors = deepcopy(context.catalogs["predictor_makeover_vendors"])
    schedule_exclusion = deepcopy(
        context.catalogs["predictor_makeover_schedule_exclusions"]
    )
    racer_names = [
        "Speed Rooster",
        "King Sting",
        "Shoebiscuit",
        "Escar-go",
        "Cactus Crawler",
    ]
    if offset is None:
        offset = save.get("year") - 1
    year = offset + 1
    vendor = {"1": [], "2": []}
    racers = {"0": [], "1": [], "2": []}
    d = 0
    while d < 3:
        day = 112 * offset + 15 + d
        vendor_pool = []
        c = 0
        while c < len(save.get("characters")):
            if not str(save.get("characters")[int(c)]) in possible_vendors:
                c += 1
                continue
            if save.get("characters")[int(c)] == "Kent" and year < 2:
                c += 1
                continue
            if save.get("characters")[int(c)] == "Leo" and (not save.get("leoMoved")):
                c += 1
                continue
            if str(save.get("characters")[int(c)]) in schedule_exclusion.get(str(d)):
                c += 1
                continue
            vendor_pool.append(save.get("characters")[int(c)])
            c += 1
        rng = SystemRandom(
            random_seed(day, save.get("gameID") / 2, legacy=save["useLegacyRandom"])
        )
        k = 0
        while k < d:
            m = 0
            while m < 2:
                index = rng.next(len(vendor_pool))
                remove_slice(vendor_pool, index, 1)
                m += 1
            k += 1
        i = 1
        while i <= 2:
            index = rng.next(len(vendor_pool))
            vendor.get(str(i)).append(vendor_pool[int(index)])
            remove_slice(vendor_pool, index, 1)
            i += 1
        racer_pool = [0, 1, 2, 3, 4]
        i = 0
        while i < 3:
            index = rng.next(len(racer_pool))
            racers.get(str(d)).append(racer_names[int(racer_pool[int(index)])])
            remove_slice(racer_pool, index, 1)
            i += 1
        d += 1
    d = 0
    while d < 3:
        capture(
            context,
            "predictMakeover",
            {
                "day": 112 * offset + 15 + d,
                "d": d,
                "racers": racers,
                "racerNames": racer_names,
                "vendor": vendor,
            },
        )
        d += 1
    if not save.get("mp_ids") is None and len(save.get("mp_ids")) > 0:
        if save.get("gender")[0] == "":
            player = 0
            while player < len(save.get("mp_ids")):
                set_slot(save.get("gender"), player, "Female")
                player += 1
        player = 0
        while player < len(save.get("mp_ids")):
            seed = int32(save.get("mp_ids")[int(player)] + year)
            rng = SystemRandom(random_seed(seed, legacy=save["useLegacyRandom"]))
            parts = [rng.next(24), rng.next(24), rng.next(16)]
            capture(
                context,
                "predictMakeover",
                {"year": year, "player": player, "parts": parts},
            )
            player += 1
        player = 0
        while player < len(save.get("mp_ids")):
            outfit = {}
            d = 0
            while d < 3:
                day = 112 * offset + 15 + d
                rng = SystemRandom(
                    random_seed(
                        day,
                        save.get("gameID") / 2,
                        year,
                        legacy=save["useLegacyRandom"],
                    )
                )
                if rng.double() < 0.75:
                    umid = int32(save.get("mp_ids")[int(player)])
                    rng = SystemRandom(
                        random_seed(
                            day,
                            save.get("gameID") / 2,
                            year,
                            umid,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                roll = rng.double()
                set_slot(
                    outfit,
                    d,
                    makeover_choices.get(str(save.get("gender")[int(player)]))[
                        int(
                            floor(
                                roll
                                * len(
                                    makeover_choices.get(
                                        str(save.get("gender")[int(player)])
                                    )
                                )
                            )
                        )
                    ],
                )
                if d == 1:
                    rng = SystemRandom(
                        random_seed(
                            day, save.get("gameID") / 2, legacy=save["useLegacyRandom"]
                        )
                    )
                    if rng.double() < 0.03:
                        set_slot(
                            outfit,
                            d,
                            {
                                "hat": "Laurel Wreath Crown",
                                "shirt": "Toga Shirt",
                                "pants": "Skirt",
                                "colors": {"pants": "#f7f5cd"},
                            },
                        )
                d += 1
            d = 0
            while d < 3:
                capture(
                    context,
                    "predictMakeover",
                    {
                        "day": 112 * offset + 15 + d,
                        "year": year,
                        "player": player,
                        "d": d,
                        "outfit": outfit[str(d)],
                    },
                )
                d += 1
            player += 1
    else:
        outfit = [[], []]
        d = 0
        while d < 3:
            day = 112 * offset + 15 + d
            rng = SystemRandom(
                random_seed(
                    day, save.get("gameID") / 2, year, legacy=save["useLegacyRandom"]
                )
            )
            rng.double()
            roll = rng.double()
            set_slot(
                outfit[0],
                d,
                makeover_choices.get("Female")[
                    int(floor(roll * len(makeover_choices.get("Female"))))
                ],
            )
            set_slot(
                outfit[1],
                d,
                makeover_choices.get("Male")[
                    int(floor(roll * len(makeover_choices.get("Male"))))
                ],
            )
            if d == 1:
                rng = SystemRandom(
                    random_seed(
                        day, save.get("gameID") / 2, legacy=save["useLegacyRandom"]
                    )
                )
                if rng.double() < 0.03:
                    set_slot(
                        outfit[0],
                        d,
                        {
                            "hat": "Laurel Wreath Crown",
                            "shirt": "Toga Shirt",
                            "pants": "Skirt",
                            "colors": {"pants": "#f7f5cd"},
                        },
                    )
                    set_slot(
                        outfit[1],
                        d,
                        {
                            "hat": "Laurel Wreath Crown",
                            "shirt": "Toga Shirt",
                            "pants": "Skirt",
                            "colors": {"pants": "#f7f5cd"},
                        },
                    )
            d += 1
        d = 0
        while d < 3:
            capture(
                context, "predictMakeover", {"year": year, "d": d, "outfit": outfit}
            )
            d += 1
        d = 0
        while d < 3:
            capture(
                context, "predictMakeover", {"year": year, "d": d, "outfit": outfit}
            )
            d += 1
    return None


def predict_calico_jack(context, is_search=None, offset=None, game_offset=0):
    save = context.save
    (
        advice,
        auto_bust,
        c1,
        c2,
        chance,
        choice,
        day_of_month,
        dealer_start,
        dealer_total,
        distance,
        g,
        have_push,
        hit,
        i,
        min_roll,
        next,
        num_played,
        page_size,
        player_total,
        r,
        rng,
        roll,
        sb_roll,
        start_hand,
        super_bust,
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
        None,
        None,
        None,
    )
    page_size = context.count or 20
    if offset is None:
        offset = save.get("daysPlayed") + save.get("dayAdjust")
    day_of_month = fmod(offset, 28)
    if not day_of_month != 0:
        day_of_month = 28
    g = 1
    while g <= page_size:
        num_played = game_offset + g
        advice = "LOSS (Unavoidable)"
        if compare_version(save.get("version"), "1.6") >= 0:
            rng = SystemRandom(
                random_seed(
                    num_played,
                    offset,
                    save.get("gameID"),
                    legacy=save["useLegacyRandom"],
                )
            )
        else:
            rng = SystemRandom(num_played + offset + save.get("gameID"))
        dealer_start = rng.next(1, 12) + rng.next(1, 10)
        c1 = rng.next(1, 12)
        c2 = rng.next(1, 10)
        start_hand = f"{c1} and {c2}"
        player_total = c1 + c2
        roll = []
        i = 0
        while i < 60:
            set_slot(roll, i, rng.double())
            i += 1
        r = 0
        hit = 0
        choice = []
        while player_total < 21:
            choice.append({"t": player_total, "r": r, "h": (hit := (hit + 1)) - 1})
            next = floor(9 * roll[int((r := (r + 1)) - 1)] + 1)
            distance = 21 - player_total
            if (distance > 1 and distance < 6) and roll[
                int((r := (r + 1)) - 1)
            ] < 1 / distance:
                next = distance if roll[int((r := (r + 1)) - 1)] < 0.5 else distance - 1
            player_total = player_total + next
        if player_total == 21:
            advice = f"WIN: Hit {hit} time{('' if hit == 1 else 's')} to reach 21"
        else:
            have_push = False
            i = 0
            while i < len(choice):
                player_total = choice[int(i)].get("t")
                r = choice[int(i)].get("r")
                dealer_total = dealer_start
                super_bust = ""
                while dealer_total < 18 or dealer_total < player_total:
                    next = floor(9 * roll[int((r := (r + 1)) - 1)] + 1)
                    distance = 21 - dealer_total
                    auto_bust = False
                    match player_total:
                        case 20:
                            auto_bust = roll[int((r := (r + 1)) - 1)] < 0.5
                        case 20 | 19:
                            auto_bust = roll[int((r := (r + 1)) - 1)] < 0.25
                        case 20 | 19 | 18:
                            auto_bust = roll[int((r := (r + 1)) - 1)] < 0.1
                    if auto_bust:
                        next = floor(distance + 3 * roll[int((r := (r + 1)) - 1)] + 1)
                    min_roll = 0.0005
                    chance = max(
                        0.0005,
                        0.001
                        + save.get("dailyLuck") / 20
                        + save.get("luckLevel") * 0.002,
                    )
                    sb_roll = roll[int((r := (r + 1)) - 1)]
                    if sb_roll < min_roll:
                        next = 999
                        super_bust = " Guaranteed super bust with 3x winnings"
                    elif sb_roll < chance:
                        next = 999
                        super_bust = " Probable super bust with 3x winnings"
                    dealer_total = dealer_total + next
                if dealer_total > 21:
                    if choice[int(i)].get("h") == 0:
                        advice = f"WIN: Stand at initial {player_total}"
                    else:
                        advice = f"WIN: Hit {choice[int(i)].get('h')} time{('' if choice[int(i)].get('h') == 1 else 's')} and stand at {player_total}"
                    break
                elif dealer_total == player_total and (not have_push):
                    have_push = True
                    advice = f"TIE: Hit {choice[int(i)].get('h')} time{('' if choice[int(i)].get('h') == 1 else 's')} and stand at {player_total}"
                advice = f"{advice}{super_bust}"
                i += 1
        capture(
            context,
            "predictCalicoJack",
            {
                "numPlayed": num_played,
                "startHand": start_hand,
                "dealerStart": dealer_start,
                "choice": choice,
                "advice": advice,
                "chance": chance,
            },
        )
        g += 1
    return None
