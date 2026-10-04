"""Native shop stock prediction rules (MouseyPounds, MIT; predictor b9e7c71)."""

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


def predict_wallpaper(context, is_search=None, offset=None):
    save = context.save
    day, eq_j, eq_p, fl_j, fl_p, rng_j, rng_p, week_day, wp_j, wp_p = (
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
    if offset is None:
        offset = 7 * floor((save.get("daysPlayed") - 1) / 7)
    week_day = 1
    while week_day < 8:
        day = week_day + offset
        if compare_version(save.get("version"), "1.6") >= 0:
            rng_p = SystemRandom(
                random_seed(
                    day + save.get("dayAdjust"),
                    save.get("gameID") / 2,
                    legacy=save["useLegacyRandom"],
                )
            )
            rng_j = SystemRandom(
                random_seed(
                    day + save.get("dayAdjust"),
                    save.get("gameID") / 2,
                    legacy=save["useLegacyRandom"],
                )
            )
            wp_p = get_random_wall_floor(context, rng_p, 0, 111, 9, {"21": True})[0]
            fl_p = 1 + get_random_wall_floor(context, rng_p, 0, 55, 22)[0]
            wp_j = get_random_wall_floor(context, rng_j, 0, 111, 9, {"21": True})[0]
            fl_j = 1 + get_random_wall_floor(context, rng_j, 0, 39, 48)[0]
        else:
            rng_p = SystemRandom(day + save.get("gameID") / 2 + save.get("dayAdjust"))
            rng_j = SystemRandom(
                day + save.get("gameID") / 2 + 1 + save.get("dayAdjust")
            )
            wp_p = rng_p.next(112)
            fl_p = 1 + rng_p.next(40)
            wp_j = rng_j.next(112)
            if wp_j == 21:
                wp_j = 22
            fl_j = 1 + rng_j.next(40)
        if str(wp_p) in save.get("wallpaperEquiv"):
            eq_p = save.get("wallpaperEquiv").get(str(wp_p))
        else:
            eq_p = "(No valid equivalence)"
        wp_p += 1
        if str(wp_j) in save.get("wallpaperEquiv"):
            eq_j = save.get("wallpaperEquiv").get(str(wp_j))
        else:
            eq_j = "(No valid equivalence)"
        wp_j += 1
        capture(
            context,
            "predictWallpaper",
            {
                "day": day,
                "wp_p": wp_p,
                "fl_p": fl_p,
                "wp_j": wp_j,
                "fl_j": fl_j,
                "eq_p": eq_p,
                "eq_j": eq_j,
            },
        )
        week_day += 1
    return None


def get_cart_item(context, rng=None, seen_items=None):
    save = context.save
    failsafe, item_i_d, keep_going, the_item = (None, None, None, None)
    the_item = {}
    item_i_d = rng.next(2, 790)
    if compare_version(save.get("version"), "1.4") >= 0:
        keep_going = True
        while keep_going:
            item_i_d += 1
            item_i_d = fmod(item_i_d, 790)
            if str(item_i_d) in save.get("cartItems_1_4"):
                the_item["name"] = save.get("cartItems_1_4").get(str(item_i_d))
                the_item["price"] = max(
                    rng.next(1, 11) * 100,
                    save.get("objects").get(str(f"_{item_i_d}")).get("price")
                    * rng.next(3, 6),
                )
                the_item["qty"] = 5 if rng.double() < 0.1 else 1
                if not the_item.get("name") in seen_items:
                    set_slot(seen_items, the_item.get("name"), 1)
                    keep_going = False
    else:
        the_item["name"] = save.get("cartItems").get(str(item_i_d))
        failsafe = 0
        while (failsafe := (failsafe + 1)) - 1 < 800 and (
            not str(f"_{item_i_d}") in save.get("objects")
            or save.get("objects").get(str(f"_{item_i_d}")).get("name")
            != the_item.get("name")
        ):
            item_i_d += 1
            item_i_d = fmod(item_i_d, 790)
        the_item["price"] = max(
            rng.next(1, 11) * 100,
            save.get("objects").get(str(f"_{item_i_d}")).get("price") * rng.next(3, 6),
        )
        the_item["qty"] = 5 if rng.double() < 0.1 else 1
    the_item["item_id"] = f"(O){item_i_d}"
    return the_item


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
        start_day,
    ) = (None, None, None, None, None, None, None, None, None, None, None, None, None)
    is_night_market = False
    if compare_version(save.get("version"), "1.6") >= 0:
        return predict_cart_1_6(context, is_search, offset)
    if offset is None or offset == "":
        offset = 7 * floor((save.get("daysPlayed") - 1) / 7)
    if compare_version(save.get("version"), "1.3") >= 0 and fmod(offset, 112) == 94:
        is_night_market = True
        start_day = 0
    else:
        is_night_market = False
        start_day = 4
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
    while not str(slot) in save.get("cartFurniture"):
        slot = rng_first.next(0, 1613)
    item = save.get("cartFurniture").get(str(slot))
    price = rng_first.next(1, 11) * 250
    capture(context, "predictCart", {"day": offset + 7, "item": item, "price": price})
    if is_night_market:
        slot = -1
        while not str(slot) in save.get("cartFurniture"):
            slot = rng_mid.next(0, 1613)
        item = save.get("cartFurniture").get(str(slot))
        price = rng_mid.next(1, 11) * 250
        capture(
            context, "predictCart", {"day": offset + 5, "item": item, "price": price}
        )
    slot = -1
    while not str(slot) in save.get("cartFurniture"):
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


def get_random_items(
    context,
    rng=None,
    type=None,
    min=None,
    max=None,
    require_price=None,
    is_random_sale=None,
    do_category_checks=False,
    how_many=1,
):
    save = context.save
    id, index, key, selected_items, shuffled_items, slot = (
        None,
        None,
        None,
        None,
        None,
        None,
    )
    shuffled_items = {}
    for _key82 in ordered_keys(save.get(str(type))):
        id = _key82
        key = rng.next()
        if invalid_number(save.get(str(type)).get(str(id)).get("id")):
            continue
        if require_price and save.get(str(type)).get(str(id)).get("price") == 0:
            continue
        if is_random_sale and save.get(str(type)).get(str(id)).get("offlimits"):
            continue
        index = int(save.get(str(type)).get(str(id)).get("id"))
        if index >= min and index <= max:
            shuffled_items[str(key)] = id
    selected_items = []
    slot = 1
    for _key86 in ordered_keys(shuffled_items):
        key = _key86
        if do_category_checks and (
            save.get(str(type)).get(str(shuffled_items.get(str(key)))).get("category")
            >= 0
            or save.get(str(type))
            .get(str(shuffled_items.get(str(key))))
            .get("category")
            == -999
        ):
            continue
        if do_category_checks and (
            (
                save.get(str(type)).get(str(shuffled_items.get(str(key)))).get("type")
                == "Arch"
                or save.get(str(type))
                .get(str(shuffled_items.get(str(key))))
                .get("type")
                == "Minerals"
            )
            or save.get(str(type)).get(str(shuffled_items.get(str(key)))).get("type")
            == "Quest"
        ):
            continue
        selected_items.append(shuffled_items.get(str(key)))
        if (slot := (slot + 1)) - 1 >= how_many:
            break
    return selected_items


def get_random_wall_floor(
    context, rng=None, min=None, max=None, extra=None, exclude={}, how_many=1
):
    id, key, selected_items, shuffled_items, slot = (None, None, None, None, None)
    shuffled_items = {}
    id = min
    while id <= max + extra:
        key = rng.next()
        shuffled_items[str(key)] = id
        id += 1
    selected_items = []
    slot = 1
    for _key93 in ordered_keys(shuffled_items):
        key = _key93
        if (
            str(shuffled_items.get(str(key))) in exclude
            or shuffled_items.get(str(key)) > max
        ):
            continue
        selected_items.append(shuffled_items.get(str(key)))
        if (slot := (slot + 1)) - 1 >= how_many:
            break
    return selected_items


def predict_cart_1_6(context, is_search=None, offset=None):
    save = context.save
    (
        cart,
        d,
        day_of_prediction,
        day_of_year,
        days,
        item,
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
    if day_of_year == 94 or day_of_year == 10:
        days = [5, 6, 7]
    else:
        days = [5, 7]
    month = floor(offset / 28)
    d = 0
    d = 0
    cart = {}
    d = 0
    while d < len(days):
        cart[str(d)] = {}
        cart.get(str(d))["rng"] = SystemRandom(
            random_seed(
                offset + days[int(d)] + save.get("dayAdjust"),
                save.get("gameID") / 2,
                legacy=save["useLegacyRandom"],
            )
        )
        cart.get(str(d))["seenRareSeed"] = False
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
            if visits_now == 0:
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
    if save.get("ccComplete"):
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
    if save.get("ccComplete") or save.get("jojaComplete"):
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
                save.get("gameID") / 2,
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
                save.get("gameID") / 2,
                legacy=save["useLegacyRandom"],
            )
        )
        rng_synced = SystemRandom(
            random_seed(
                hash_string("krobus_bread"),
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


def predict_sandy(context, is_search=None, offset=None):
    save = context.save
    (
        cc_shirts,
        day,
        day_of_week,
        extra,
        item,
        num_i_d,
        oasis_shirts,
        result,
        rng,
        sprite_i_d,
        this_roll,
    ) = (None, None, None, None, None, None, None, None, None, None, None)
    cc_shirts = [
        1019,
        1022,
        1023,
        1040,
        1041,
        1043,
        1045,
        1046,
        1049,
        1054,
        1056,
        1060,
        1076,
        1080,
        1082,
        1084,
        1087,
        1090,
        1108,
        1109,
        1110,
    ]
    oasis_shirts = [1118, 1119, 1120, 1121]
    if offset is None or offset == "":
        offset = 7 * floor((save.get("daysPlayed") - 1) / 7)
    day_of_week = 1
    while day_of_week < 8:
        day = day_of_week + offset
        extra = ""
        num_i_d = 0
        if compare_version(save.get("version"), "1.6") >= 0:
            rng = SystemRandom(
                random_seed(
                    day + save.get("dayAdjust"),
                    save.get("gameID") / 2,
                    legacy=save["useLegacyRandom"],
                )
            )
            result = get_random_items(context, rng, "shirts", 1000, 1126, True, True)
            sprite_i_d = int(save.get("shirts").get(str(result[0])).get("id")) - 999
            num_i_d = int(save.get("shirts").get(str(result[0])).get("id"))
            item = f"{save.get('shirts').get(str(result[0])).get('name')} ID: (S){save.get('shirts').get(str(result[0])).get('id')}"
        else:
            rng = SystemRandom(save.get("gameID") / 2 + day + save.get("dayAdjust"))
            this_roll = 1000 + rng.next(127)
            sprite_i_d = this_roll - 999
            num_i_d = this_roll
            item = f"{save.get('shirts').get(str(f'_{this_roll}')).get('name')} ID: {this_roll}"
        if num_i_d in oasis_shirts:
            extra = "  Oasis exclusive"
        elif num_i_d in cc_shirts:
            extra = f"  Character Creator option {sprite_i_d}"
        capture(
            context,
            "predictSandy",
            {
                "day": day,
                "item": item,
                "numID": num_i_d,
                "spriteID": sprite_i_d,
                "extra": extra,
            },
        )
        day_of_week += 1
    return None


def predict_bookseller(context, is_search=None, offset=None):
    save = context.save
    (
        books_left,
        d,
        days,
        days_played,
        i,
        month,
        picked,
        possible_days,
        rand_book_list,
        rng,
        rng_synced,
        season_index,
        skill_book_list,
        stock,
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
    )
    skill_book_list = [
        "Stardew Valley Almanac",
        "Bait And Bobber",
        "Woodcutter's Weekly",
        "Mining Monthly",
        "Combat Quarterly",
    ]
    rand_book_list = deepcopy(context.catalogs["predictor_bookseller_random_books"])
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    month = floor(offset / 28)
    season_index = fmod(month, 4)
    year = 1 + floor(offset / 112)
    rng = SystemRandom(
        random_seed(
            year * 11, save.get("gameID"), season_index, legacy=save["useLegacyRandom"]
        )
    )
    possible_days = []
    match season_index:
        case 0:
            possible_days = [11, 12, 21, 22, 25]
        case 0 | 1:
            possible_days = [9, 12, 18, 25, 27]
        case 0 | 1 | 2:
            possible_days = [4, 7, 8, 9, 12, 19, 22, 25]
        case 0 | 1 | 2 | 3:
            possible_days = [5, 11, 12, 19, 22, 24]
    i = rng.next(len(possible_days))
    days = sorted(
        [
            possible_days[int(i)],
            possible_days[
                int(floor(fmod(i + len(possible_days) / 2, len(possible_days))))
            ],
        ]
    )
    d = 0
    d = 0
    stock = {}
    d = 0
    while d < len(days):
        days_played = offset + days[int(d)] + save.get("dayAdjust")
        stock[str(d)] = {}
        rng = SystemRandom(
            random_seed(
                days_played, save.get("gameID") / 2, legacy=save["useLegacyRandom"]
            )
        )
        rng_synced = SystemRandom(
            random_seed(
                hash_string("purplebookSale"),
                save.get("gameID"),
                days_played,
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.25:
            stock.get(str(d))["purplebook"] = {"name": "Book Of Stars", "price": 15000}
        else:
            stock.get(str(d))["purplebook"] = None
        books_left = skill_book_list[:]
        rng_synced = SystemRandom(
            random_seed(
                hash_string("thirdBookSale"),
                save.get("gameID"),
                days_played,
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.6:
            picked = remove_slice(books_left, rng.next(len(books_left)), 1)
            stock.get(str(d))["skill60pct"] = {"name": picked[0], "price": 10000}
        else:
            stock.get(str(d))["skill60pct"] = None
        rng_synced = SystemRandom(
            random_seed(
                hash_string("secondBookSale"),
                save.get("gameID"),
                days_played,
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.8:
            picked = remove_slice(books_left, rng.next(len(books_left)), 1)
            stock.get(str(d))["skill80pct"] = {"name": picked[0], "price": 8000}
        else:
            stock.get(str(d))["skill80pct"] = None
        picked = remove_slice(books_left, rng.next(len(books_left)), 1)
        stock.get(str(d))["skillAlways"] = {"name": picked[0], "price": 5000}
        if year >= 3:
            picked = rand_book_list[int(rng.next(len(rand_book_list)))]
            stock.get(str(d))["y3"] = {"name": picked, "price": 20000}
        else:
            stock.get(str(d))["y3"] = None
        rng_synced = SystemRandom(
            random_seed(
                hash_string("bookExtraForaging"),
                save.get("gameID"),
                days_played,
                legacy=save["useLegacyRandom"],
            )
        )
        if rng_synced.double() < 0.33:
            stock.get(str(d))["foragebook"] = {
                "name": "Woodcutter's Weekly",
                "price": 8000,
            }
        else:
            stock.get(str(d))["foragebook"] = None
        d += 1
    capture(context, "predictBookseller", {"days": days, "stock": stock})
    d = 0
    d = 0
    d = 0
    d = 0
    d = 0
    d = 0
    return None
