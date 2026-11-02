"""Festival rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    deepcopy,
    floor,
    int32,
    random_seed,
    remove_slice,
    set_slot,
    trunc_div,
)


def _capture_makeover(context, facts):
    if context.save.get("hostDesertUnlocked") is False:
        facts = {
            **facts,
            "availability": "requires_desert_access",
            "conditions": "Conditional on the host repairing the bus before attending the Desert Festival (Spring 15–17, from 10:00)",
        }
    capture(context, "predictMakeover", facts)


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
            if str(save.get("characters")[int(c)]) not in possible_vendors:
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
            random_seed(
                day, trunc_div(save["gameID"], 2), legacy=save["useLegacyRandom"]
            )
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
        _capture_makeover(
            context,
            {
                "day": 112 * offset + 15 + d,
                "d": d,
                "racers": racers,
                "racerNames": racer_names,
                "vendor": vendor,
            },
        )
        d += 1
    if save.get("mp_ids") is not None and len(save.get("mp_ids")) > 0:
        if save.get("gender")[0] == "":
            player = 0
            while player < len(save.get("mp_ids")):
                if (
                    context.selected_players is not None
                    and player not in context.selected_players
                ):
                    player += 1
                    continue
                set_slot(save.get("gender"), player, "Female")
                player += 1
        player = 0
        while player < len(save.get("mp_ids")):
            if (
                context.selected_players is not None
                and player not in context.selected_players
            ):
                player += 1
                continue
            seed = random_seed(
                save["mp_ids"][player], year, legacy=save["useLegacyRandom"]
            )
            rng = SystemRandom(random_seed(seed, legacy=save["useLegacyRandom"]))
            parts = [rng.next(24), rng.next(24), rng.next(16)]
            _capture_makeover(
                context,
                {"year": year, "player": player, "parts": parts},
            )
            player += 1
        player = 0
        while player < len(save.get("mp_ids")):
            if (
                context.selected_players is not None
                and player not in context.selected_players
            ):
                player += 1
                continue
            outfit = {}
            d = 0
            while d < 3:
                day = 112 * offset + 15 + d
                rng = SystemRandom(
                    random_seed(
                        day,
                        trunc_div(save["gameID"], 2),
                        year,
                        legacy=save["useLegacyRandom"],
                    )
                )
                if rng.double() < 0.75:
                    umid = int32(save.get("mp_ids")[int(player)])
                    rng = SystemRandom(
                        random_seed(
                            day,
                            trunc_div(save["gameID"], 2),
                            year,
                            umid,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                roll = rng.double()
                choices = makeover_pool(context, player)
                set_slot(outfit, d, choices[int(floor(roll * len(choices)))])
                if d == 1:
                    rng = SystemRandom(
                        random_seed(
                            day,
                            trunc_div(save["gameID"], 2),
                            legacy=save["useLegacyRandom"],
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
                _capture_makeover(
                    context,
                    {
                        "day": 112 * offset + 15 + d,
                        "year": year,
                        "player": player,
                        "d": d,
                        "outfit": outfit[str(d)],
                        "equipmentAssumption": save.get("equippedMakeoverItems", ())[
                            player
                        ]
                        if save.get("equippedMakeoverItems")
                        else (),
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
                    day,
                    trunc_div(save["gameID"], 2),
                    year,
                    legacy=save["useLegacyRandom"],
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
                        day,
                        trunc_div(save["gameID"], 2),
                        legacy=save["useLegacyRandom"],
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
            _capture_makeover(
                context, "predictMakeover", {"year": year, "d": d, "outfit": outfit}
            )
            d += 1
        d = 0
        while d < 3:
            _capture_makeover(
                context, "predictMakeover", {"year": year, "d": d, "outfit": outfit}
            )
            d += 1
    return None


def makeover_pool(context, player):
    """Filter before drawing, as DesertFestival.ReceiveMakeOver does."""
    save = context.save
    gender = save["gender"][player]
    choices = deepcopy(context.catalogs["predictor_makeover_choices"][gender])
    raw = save.get("makeoverOutfits")
    if raw is not None:
        gender_id = 0 if gender == "Male" else 1
        rows = [row for row in raw if row.get("Gender") in (None, gender_id)]
        # Bundled names are presentation only; selection follows actual table order.
        choices = []
        for row in rows:
            choice = {"item_ids": {}, "colors": {}}
            for part in row["OutfitParts"]:
                if part.get("Gender") not in (None, gender_id):
                    continue
                identifier = part["ItemId"]
                kind = {"H": "hat", "S": "shirt", "P": "pants"}.get(identifier[1:2])
                if kind is None:
                    continue
                choice["item_ids"][kind] = identifier
                choice[kind] = part["Id"]
                if part.get("Color"):
                    color = part["Color"]
                    components = color.split()
                    if len(components) == 3 and all(
                        c.isdigit() and 0 <= int(c) <= 255 for c in components
                    ):
                        color = "#" + "".join(f"{int(c):02x}" for c in components)
                    choice["colors"][kind] = color
            choices.append(choice)
    else:
        shirts = {
            row["name"]: "(S)" + str(row["id"]) for row in save["shirts"].values()
        }
        for choice in choices:
            choice.setdefault("item_ids", {})
            if choice.get("shirt") in shirts:
                choice["item_ids"].setdefault("shirt", shirts[choice["shirt"]])
            for part, color in choice.get("colors", {}).items():
                if color.startswith("#"):
                    choice["colors"][part] = color.replace(" ", "0")
    equipped = save.get("equippedMakeoverItems", ())
    if equipped:
        for kind, identifier, name in equipped[player]:
            part, prefix = ("hat", "(H)") if kind == "hat" else ("shirt", "(S)")
            qualified = (
                identifier
                if identifier and identifier.startswith("(")
                else prefix + (identifier or "")
            )
            choices = [
                choice
                for choice in choices
                if choice.get("item_ids", {}).get(part) != qualified
                and not (raw is None and name and choice.get(part) == name)
            ]
    if not choices:
        from stardew.domain.errors import FeatureUnavailable

        raise FeatureUnavailable(
            "No eligible makeover outfit remains for the saved equipment."
        )
    return choices
