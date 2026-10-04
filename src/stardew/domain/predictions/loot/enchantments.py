"""Enchantments rules adapted from MouseyPounds (MIT; predictor b9e7c71)."""

from ..report_support import (
    PredictionContext,
    SystemRandom,
    capture,
    compare_version,
    deepcopy,
    exact_seed_part,
    floor,
    random_seed,
    set_slot,
)


def predict_enchantments(
    context: PredictionContext, is_search: bool | None = None, offset: int | None = None
) -> None:
    save = context.save
    page_size = context.count or 20
    labels = ["Weapon", "Pickaxe", "Axe", "Hoe", "Watering Can", "Fishing Rod", "Pan"]
    num_columns = len(labels)
    valid_enchants = deepcopy(context.catalogs["predictor_enchantments"])
    which_player = context.player_index
    if offset is None:
        offset = page_size * floor(
            save.get("timesEnchanted")[int(which_player)] / page_size
        )
    g = 1
    while g <= page_size:
        times_enchanted = offset + g
        item = []
        if compare_version(save.get("version"), "1.6") >= 0:
            if not save.get("mp_ids") is None:
                rng = SystemRandom(
                    random_seed(
                        exact_seed_part(int(times_enchanted - 1)),
                        exact_seed_part(int(save.get("gameID"))),
                        exact_seed_part(save.get("mp_ids")[int(which_player)]),
                        legacy=save["useLegacyRandom"],
                    )
                )
            else:
                rng = SystemRandom(
                    random_seed(
                        times_enchanted - 1,
                        save.get("gameID"),
                        0,
                        legacy=save["useLegacyRandom"],
                    )
                )
        else:
            rng = SystemRandom(times_enchanted + save.get("gameID") - 1)
        rand_roll = rng.double()
        c = 0
        while c < num_columns:
            roll = floor(rand_roll * len(valid_enchants[int(c)]))
            result = valid_enchants[int(c)][int(roll)]
            set_slot(item, c, [result])
            roll2 = floor(rand_roll * (len(valid_enchants[int(c)]) - 1))
            if roll2 < roll:
                item[int(c)].append(valid_enchants[int(c)][int(roll2)])
            else:
                item[int(c)].append(valid_enchants[int(c)][int(roll2 + 1)])
            roll3 = floor(rand_roll * (len(valid_enchants[int(c)]) - 2))
            if roll3 < roll2:
                item[int(c)].append(valid_enchants[int(c)][int(roll3)])
            else:
                item[int(c)].append(valid_enchants[int(c)][int(roll3 + 2)])
            c += 1
        c = 0
        capture(
            context,
            "predictEnchantments",
            {
                "timesEnchanted": times_enchanted,
                "whichPlayer": which_player,
                "item": item,
                "labels": labels,
                "validEnchants": valid_enchants,
                "randRoll": rand_roll,
            },
        )
        g += 1
    return None
