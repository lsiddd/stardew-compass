"""Cart rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    fmod,
    hash_string,
    random_seed,
    trunc_div,
)
from .shop_selection import get_cart_item, get_random_items


def predict_cart(context, is_search=None, offset=None):
    save = context.save
    (
        is_night_market,
        item,
        month,
        price,
        qty,
        rng_first,
        rng_last,
        rng_mid,
        seen_items_first,
        seen_items_last,
        seen_items_mid,
        slot,
        _start_day,
    ) = (None, None, None, None, None, None, None, None, None, None, None, None, None)
    is_night_market = False
    if compare_version(save.get("version"), "1.6") >= 0:
        return predict_cart_1_6(context, is_search, offset)
    if offset is None or offset == "":
        offset = 7 * floor((save.get("daysPlayed") - 1) / 7)
    if compare_version(save.get("version"), "1.3") >= 0 and fmod(offset, 112) == 94:
        is_night_market = True
    else:
        is_night_market = False
    month = floor(offset / 28)
    rng_first = SystemRandom(save.get("gameID") + offset + 5 + save.get("dayAdjust"))
    if is_night_market:
        rng_mid = SystemRandom(save.get("gameID") + offset + 6 + save.get("dayAdjust"))
    rng_last = SystemRandom(save.get("gameID") + offset + 7 + save.get("dayAdjust"))
    seen_items_first = {}
    seen_items_mid = {}
    seen_items_last = {}
    slot = 1
    while slot <= 10:
        item = get_cart_item(context, rng_first, seen_items_first)
        capture(
            context,
            "predictCart",
            {"day": offset + 7, "item": item, "qty": qty, "price": price},
        )
        if is_night_market:
            item = get_cart_item(context, rng_mid, seen_items_mid)
            capture(
                context,
                "predictCart",
                {"day": offset + 6, "item": item, "qty": qty, "price": price},
            )
        item = get_cart_item(context, rng_last, seen_items_last)
        capture(
            context,
            "predictCart",
            {"day": offset + 7, "item": item, "qty": qty, "price": price},
        )
        slot += 1
    slot = -1
    while str(slot) not in save.get("cartFurniture"):
        slot = rng_first.next(0, 1613)
    item = save.get("cartFurniture").get(str(slot))
    price = rng_first.next(1, 11) * 250
    capture(context, "predictCart", {"day": offset + 7, "item": item, "price": price})
    if is_night_market:
        slot = -1
        while str(slot) not in save.get("cartFurniture"):
            slot = rng_mid.next(0, 1613)
        item = save.get("cartFurniture").get(str(slot))
        price = rng_mid.next(1, 11) * 250
        capture(
            context, "predictCart", {"day": offset + 5, "item": item, "price": price}
        )
    slot = -1
    while str(slot) not in save.get("cartFurniture"):
        slot = rng_last.next(0, 1613)
    item = save.get("cartFurniture").get(str(slot))
    price = rng_last.next(1, 11) * 250
    capture(context, "predictCart", {"day": offset + 7, "item": item, "price": price})
    if fmod(month, 4) < 2:
        item = "Rare Seed"
        price = 1000
        qty = 5 if rng_first.double() < 0.1 else 1
        capture(
            context,
            "predictCart",
            {"day": offset + 7, "item": item, "qty": qty, "price": price},
        )
        if is_night_market:
            qty = 5 if rng_mid.double() < 0.1 else 1
            capture(
                context,
                "predictCart",
                {"day": offset + 6, "item": item, "qty": qty, "price": price},
            )
        qty = 5 if rng_last.double() < 0.1 else 1
        capture(
            context,
            "predictCart",
            {"day": offset + 7, "item": item, "qty": qty, "price": price},
        )
    else:
        if rng_first.double() < 0.4:
            item = "Rarecrow (Snowman)"
            qty = 1
            price = "4000g"
        else:
            item = "(None)"
            qty = "--"
            price = "--"
        capture(
            context,
            "predictCart",
            {"day": offset + 5, "item": item, "qty": qty, "price": price},
        )
        if is_night_market:
            if rng_mid.double() < 0.4:
                item = "Rarecrow (Snowman)"
                qty = 1
                price = "4000g"
            else:
                item = "(None)"
                qty = "--"
                price = "--"
            capture(
                context,
                "predictCart",
                {"day": offset + 6, "item": item, "qty": qty, "price": price},
            )
        if rng_last.double() < 0.4:
            item = "Rarecrow (Snowman)"
            qty = 1
            price = "4000g"
        else:
            item = "(None)"
            qty = "--"
            price = "--"
        capture(
            context,
            "predictCart",
            {"day": offset + 7, "item": item, "qty": qty, "price": price},
        )
    if rng_first.double() < 0.25:
        item = "Coffee Bean"
        qty = 1
        price = "2500g"
    else:
        item = "(None)"
        qty = "--"
        price = "--"
    capture(
        context,
        "predictCart",
        {"day": offset + 5, "item": item, "qty": qty, "price": price},
    )
    if is_night_market:
        if rng_mid.double() < 0.25:
            item = "Coffee Bean"
            qty = 1
            price = "2500g"
        else:
            item = "(None)"
            qty = "--"
            price = "--"
        capture(
            context,
            "predictCart",
            {"day": offset + 6, "item": item, "qty": qty, "price": price},
        )
    if rng_last.double() < 0.25:
        item = "Coffee Bean"
        qty = 1
        price = "2500g"
    else:
        item = "(None)"
        qty = "--"
        price = "--"
    capture(
        context,
        "predictCart",
        {"day": offset + 7, "item": item, "qty": qty, "price": price},
    )
    return None


def predict_cart_1_6(context, is_search=None, offset=None):
    save = context.save
    (
        cart,
        d,
        day_of_prediction,
        day_of_year,
        days,
        _item,
        month,
        name,
        pick,
        price,
        qty,
        rng_synced,
        skill_book_list,
        slot,
        visits_now,
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
    )
    skill_book_list = [
        "Stardew Valley Almanac",
        "Bait And Bobber",
        "Woodcutter's Weekly",
        "Mining Monthly",
        "Combat Quarterly",
    ]
    if offset is None or offset == "":
        offset = 7 * floor((save.get("daysPlayed") - 1) / 7)
    day_of_year = fmod(offset, 112)
    if day_of_year == 10:
        days = (
            [5, 6, 7]
            if save.get("hostDesertUnlocked", save.get("desertUnlocked"))
            else []
        )
    elif day_of_year == 94:
        days = [5, 6, 7]
    else:
        days = [5, 7]
    month = floor(offset / 28)
    d = 0
    cart = {}
    d = 0
    while d < len(days):
        cart[str(d)] = {}
        cart.get(str(d))["rng"] = SystemRandom(
            random_seed(
                offset + days[int(d)] + save.get("dayAdjust"),
                trunc_div(save["gameID"], 2),
                legacy=save["useLegacyRandom"],
            )
        )
        cart.get(str(d))["seenRareSeed"] = False
        cart.get(str(d))["seenItemIds"] = set()
        cart.get(str(d))["selectedItems"] = {}
        pick = get_random_items(
            context,
            cart.get(str(d)).get("rng"),
            "objects",
            2,
            789,
            True,
            True,
            True,
            10,
        )
        slot = 1
        while slot <= 10:
            cart.get(str(d)).get("selectedItems")[str(slot)] = {}
            cart.get(str(d)).get("selectedItems").get(str(slot))["item_id"] = (
                "(O)" + pick[int(slot - 1)].removeprefix("_")
            )
            cart[str(d)]["seenItemIds"].add(
                cart[str(d)]["selectedItems"][str(slot)]["item_id"]
            )
            cart.get(str(d)).get("selectedItems").get(str(slot))["name"] = (
                save.get("objects").get(str(pick[int(slot - 1)])).get("name")
            )
            if (
                cart.get(str(d)).get("selectedItems").get(str(slot)).get("name")
                == "Rare Seed"
            ):
                cart.get(str(d))["seenRareSeed"] = True
            cart.get(str(d)).get("selectedItems").get(str(slot))["price"] = max(
                cart.get(str(d)).get("rng").next(1, 11) * 100,
                cart.get(str(d)).get("rng").next(3, 6)
                * save.get("objects").get(str(pick[int(slot - 1)])).get("price"),
            )
            cart.get(str(d)).get("selectedItems").get(str(slot))["qty"] = (
                5 if cart.get(str(d)).get("rng").double() < 0.1 else 1
            )
            slot += 1
        d += 1
    slot = 1
    while slot <= 10:
        d = 0
        while d < len(days):
            capture(
                context,
                "predictCart_1_6",
                {
                    "day": offset + days[d],
                    "item": cart[str(d)]["selectedItems"][str(slot)],
                    "slot": slot,
                },
            )
            d += 1
        slot += 1
    if save.get("originalGuarantee") >= 0:
        d = 0
        while d < len(days):
            day_of_prediction = offset + days[int(d)] + save.get("dayAdjust")
            visits_now = (
                save.get("originalGuarantee")
                - floor(day_of_prediction / 7)
                - floor((day_of_prediction + 2) / 7)
            )
            if day_of_prediction >= 99:
                visits_now += -1
            if day_of_prediction >= 100:
                visits_now += -1
            if day_of_prediction >= 101:
                visits_now += -1
            # ShopBuilder rejects an already selected ID before rolling its
            # price/stock; consuming those draws also changes the later stock.
            if visits_now == 0 and "(O)485" not in cart[str(d)]["seenItemIds"]:
                name = save.get("objects").get("_485").get("name")
                price = max(
                    cart.get(str(d)).get("rng").next(1, 11) * 100,
                    cart.get(str(d)).get("rng").next(3, 6)
                    * save.get("objects").get("_485").get("price"),
                )
                qty = 5 if cart.get(str(d)).get("rng").double() < 0.1 else 1
                capture(
                    context,
                    "predictCart_1_6",
                    {
                        "day": day_of_prediction,
                        "item": name,
                        "qty": qty,
                        "price": price,
                        "slot": "year_one_guarantee",
                    },
                )
            d += 1
    d = 0
    while d < len(days):
        pick = get_random_items(
            context, cart.get(str(d)).get("rng"), "furniture", 0, 1612, True, True
        )
        name = save.get("furniture").get(str(pick[0])).get("name")
        price = cart.get(str(d)).get("rng").next(1, 11) * 250
        capture(
            context,
            "predictCart_1_6",
            {
                "day": offset + days[d],
                "item": name,
                "item_id": "(F)" + pick[0].removeprefix("_"),
                "qty": 1,
                "price": price,
                "slot": "furniture",
            },
        )
        d += 1
    if fmod(month, 4) < 2:
        d = 0
        while d < len(days):
            if not cart.get(str(d)).get("seenRareSeed"):
                name = "Rare Seed"
                price = 1000
                qty = 5 if cart.get(str(d)).get("rng").double() < 0.1 else 1
            else:
                name = "(None)"
                price = "--"
                qty = "--"
            capture(
                context,
                "predictCart_1_6",
                {
                    "day": offset + days[d],
                    "item": name,
                    "qty": qty,
                    "price": price,
                    "slot": "seasonal",
                },
            )
            d += 1
    else:
        d = 0
        while d < len(days):
            rng_synced = SystemRandom(
                random_seed(
                    hash_string("cart_rarecrow"),
                    save.get("gameID"),
                    offset + days[int(d)] + save.get("dayAdjust"),
                    legacy=save["useLegacyRandom"],
                )
            )
            if rng_synced.double() < 0.4:
                name = "Rarecrow (Snowman)"
                price = 4000
                qty = 1
            else:
                name = "(None)"
                price = "--"
                qty = "--"
            capture(
                context,
                "predictCart_1_6",
                {
                    "day": offset + days[d],
                    "item": name,
                    "qty": qty,
                    "price": price,
                    "slot": "seasonal",
                },
            )
            d += 1
    if fmod(month, 4) > 1:
        d = 0
        while d < len(days):
            rng_synced = SystemRandom(
                random_seed(
                    hash_string("cart_coffee_bean"),
                    save.get("gameID"),
                    offset + days[int(d)] + save.get("dayAdjust"),
                    legacy=save["useLegacyRandom"],
                )
            )
            if rng_synced.double() < 0.25:
                name = "Coffee Bean"
                price = 2500
                qty = 1
            else:
                name = "(None)"
                price = "--"
                qty = "--"
            capture(
                context,
                "predictCart_1_6",
                {
                    "day": offset + days[d],
                    "item": name,
                    "qty": qty,
                    "price": price,
                    "slot": "coffee_bean",
                },
            )
            d += 1
    d = 0
    while d < len(days):
        rng_synced = SystemRandom(
            random_seed(
                hash_string("cart_fez"),
                save.get("gameID"),
                offset + days[int(d)] + save.get("dayAdjust"),
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.1:
            name = "Red Fez"
            price = 8000
            qty = 1
        else:
            name = "(None)"
            price = "--"
            qty = "--"
        capture(
            context,
            "predictCart_1_6",
            {
                "day": offset + days[d],
                "item": name,
                "qty": qty,
                "price": price,
                "slot": "red_fez",
            },
        )
        d += 1
    if save.get("hostCommunityCenterComplete", save.get("ccComplete")):
        d = 0
        while d < len(days):
            rng_synced = SystemRandom(
                random_seed(
                    hash_string("cart_jojaCatalogue"),
                    save.get("gameID"),
                    offset + days[int(d)] + save.get("dayAdjust"),
                    legacy=save["useLegacyRandom"],
                )
            )
            if rng_synced.double() < 0.1:
                name = "Joja Catalogue"
                price = 30000
                qty = 1
            else:
                name = "(None)"
                price = "--"
                qty = "--"
            capture(
                context,
                "predictCart_1_6",
                {
                    "day": offset + days[d],
                    "item": name,
                    "qty": qty,
                    "price": price,
                    "slot": "catalogue",
                },
            )
            d += 1
    if save.get("hostCommunityCenterComplete", save.get("ccComplete")) or save.get(
        "hostJojaMartComplete", save.get("jojaComplete")
    ):
        d = 0
        while d < len(days):
            rng_synced = SystemRandom(
                random_seed(
                    hash_string("cart_junimoCatalogue"),
                    save.get("gameID"),
                    offset + days[int(d)] + save.get("dayAdjust"),
                    legacy=save["useLegacyRandom"],
                )
            )
            if rng_synced.double() < 0.1:
                name = "Junimo Catalogue"
                price = 70000
                qty = 1
            else:
                name = "(None)"
                price = "--"
                qty = "--"
            capture(
                context,
                "predictCart_1_6",
                {
                    "day": offset + days[d],
                    "item": name,
                    "qty": qty,
                    "price": price,
                    "slot": "catalogue",
                },
            )
            d += 1
    d = 0
    while d < len(days):
        rng_synced = SystemRandom(
            random_seed(
                hash_string("cart_retroCatalogue"),
                save.get("gameID"),
                offset + days[int(d)] + save.get("dayAdjust"),
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.1:
            name = "Retro Catalogue"
            price = 110000
            qty = 1
        else:
            name = "(None)"
            price = "--"
            qty = "--"
        capture(
            context,
            "predictCart_1_6",
            {
                "day": offset + days[d],
                "item": name,
                "qty": qty,
                "price": price,
                "slot": "catalogue",
            },
        )
        d += 1
    if offset + save.get("dayAdjust") >= 2688:
        d = 0
        while d < len(days):
            rng_synced = SystemRandom(
                random_seed(
                    hash_string("teaset"),
                    save.get("gameID"),
                    offset + days[int(d)] + save.get("dayAdjust"),
                    legacy=save["useLegacyRandom"],
                )
            )
            if rng_synced.double() < 0.05:
                name = "Tea Set"
                price = 1000000
                qty = "∞"
            else:
                name = "(None)"
                price = "--"
                qty = "--"
            capture(
                context,
                "predictCart_1_6",
                {
                    "day": offset + days[d],
                    "item": name,
                    "qty": qty,
                    "price": price,
                    "slot": "tea_set",
                },
            )
            d += 1
    d = 0
    while d < len(days):
        rng_synced = SystemRandom(
            random_seed(
                hash_string("travelerSkillBook"),
                save.get("gameID"),
                offset + days[int(d)] + save.get("dayAdjust"),
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.05:
            name = skill_book_list[
                int(cart.get(str(d)).get("rng").next(len(skill_book_list)))
            ]
            price = 6000
            qty = 1
        else:
            name = "(None)"
            price = "--"
            qty = "--"
        capture(
            context,
            "predictCart_1_6",
            {
                "day": offset + days[d],
                "item": name,
                "qty": qty,
                "price": price,
                "slot": "skill_book",
            },
        )
        d += 1
    return None
