"""Winter Star rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    deepcopy,
    exact_seed_part,
    int32,
    random_seed,
    remove_slice,
    trunc_div,
)


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
    if save.get("names") is not None and (save.get("mp_ids") is not None):
        num_players = len(save.get("names"))
    else:
        force_old_logic = True
    player = 0
    while player < num_players:
        if (
            context.selected_players is not None
            and player not in context.selected_players
        ):
            player += 1
            continue
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
            divorced = save.get("divorcedNpcs", ())
            excluded_donors = set(divorced[player]) if divorced else set()
            excluded_donors.add(secret_santa_give_to)
            npcs = [name for name in npcs if name not in excluded_donors]
            rng = SystemRandom(
                random_seed(
                    exact_seed_part(trunc_div(int(save.get("gameID")), 2)),
                    exact_seed_part(int(year)),
                    exact_seed_part(save.get("mp_ids")[int(player)]),
                    legacy=save["useLegacyRandom"],
                )
            )
            while npcs and secret_santa_get_from == "":
                index = rng.next(len(npcs))
                pick = npcs[int(index)]
                if pick == "Marlon" or (year == 1 and pick == "Kent"):
                    remove_slice(npcs, index, 1)
                else:
                    secret_santa_get_from = pick
            if not secret_santa_get_from:
                secret_santa_get_from = secret_santa_give_to
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
