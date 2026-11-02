"""Krobus rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    hash_string,
    random_seed,
    set_slot,
    trunc_div,
)
from .shop_selection import get_random_items


def predict_krobus(context, is_search=None, offset=None):
    save = context.save
    item_ids = []
    days, i, item, price, qty, result, rng, rng_synced, this_roll = (
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
    if offset is None or offset == "":
        offset = 7 * floor((save.get("daysPlayed") - 1) / 7)
    item = ["None", "None"]
    item_ids = [None, None]
    price = [200, 0]
    qty = [5, 5]
    if compare_version(save.get("version"), "1.6") >= 0:
        rng = SystemRandom(
            random_seed(
                offset + 3 + save.get("dayAdjust"),
                trunc_div(save["gameID"], 2),
                legacy=save["useLegacyRandom"],
            )
        )
        result = get_random_items(context, rng, "objects", 698, 708, True, True)
        set_slot(
            item,
            0,
            save.get("objects").get((_selected_item_id := str(result[0]))).get("name"),
        )
        set_slot(item_ids, 0, "(O)" + str(_selected_item_id).removeprefix("_"))
        rng = SystemRandom(
            random_seed(
                offset + 6 + save.get("dayAdjust"),
                trunc_div(save["gameID"], 2),
                legacy=save["useLegacyRandom"],
            )
        )
        rng_synced = SystemRandom(
            random_seed(
                hash_string("krobus_bread"),
                save.get("gameID"),
                offset + 6 + save.get("dayAdjust"),
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.0196078431:
            set_slot(
                item,
                1,
                save.get("objects").get((_selected_item_id := "_216")).get("name"),
            )
            set_slot(item_ids, 1, "(O)" + str(_selected_item_id).removeprefix("_"))
            set_slot(price, 1, 10 * rng.next(5, 51))
        else:
            result = get_random_items(context, rng, "objects", 194, 244, True, True)
            set_slot(
                item,
                1,
                save.get("objects")
                .get((_selected_item_id := str(result[0])))
                .get("name"),
            )
            set_slot(item_ids, 1, "(O)" + str(_selected_item_id).removeprefix("_"))
            set_slot(price, 1, 10 * rng.next(5, 51))
    else:
        rng = SystemRandom(save.get("gameID") / 2 + offset + 3 + save.get("dayAdjust"))
        set_slot(item, 0, save.get("cartItems").get(str(rng.next(698, 709) - 1)))
        set_slot(item_ids, 0, None)
        rng = SystemRandom(save.get("gameID") / 2 + offset + 6 + save.get("dayAdjust"))
        this_roll = rng.next(194, 245) - 1
        if this_roll == 216:
            this_roll = 215
        set_slot(item, 1, save.get("cartItems").get(str(this_roll)))
        set_slot(item_ids, 1, None)
        set_slot(price, 1, rng.next(5, 51) * 10)
    i = 0
    while i < len(item):
        capture(
            context,
            "predictKrobus",
            {
                "days": days,
                "i": i,
                "item": item,
                "qty": qty,
                "price": price,
                "itemIDs": item_ids,
            },
        )
        i += 1
    return None
