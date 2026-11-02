"""Shop Selection rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    compare_version,
    fmod,
    invalid_number,
    ordered_keys,
    set_slot,
)


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
                if the_item.get("name") not in seen_items:
                    set_slot(seen_items, the_item.get("name"), 1)
                    keep_going = False
    else:
        the_item["name"] = save.get("cartItems").get(str(item_i_d))
        failsafe = 0
        while (failsafe := (failsafe + 1)) - 1 < 800 and (
            str(f"_{item_i_d}") not in save.get("objects")
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
    pool = context.save[str(type)]
    shuffled_items = []
    for item_id in ordered_keys(pool):
        priority = rng.next()
        item = pool[item_id]
        if invalid_number(item.get("id")):
            continue
        if require_price and item.get("price", 0) <= 0:
            continue
        if is_random_sale and item.get("offlimits"):
            continue
        index = int(item["id"])
        if index >= min and index <= max:
            shuffled_items.append((priority, item_id))
    # LINQ OrderBy is stable. Equal random priorities keep both items, in the
    # catalog's original order, instead of overwriting a dictionary entry.
    shuffled_items.sort(key=lambda entry: entry[0])
    selected_items = []
    for _, item_id in shuffled_items:
        item = pool[item_id]
        if do_category_checks and (item["category"] >= 0 or item["category"] == -999):
            continue
        if do_category_checks and item["type"] in ("Arch", "Minerals", "Quest"):
            continue
        selected_items.append(item_id)
        if len(selected_items) >= how_many:
            break
    return selected_items


def get_random_wall_floor(
    context, rng=None, min=None, max=None, extra=None, exclude=None, how_many=1
):
    if exclude is None:
        exclude = ()
    shuffled_items = [(rng.next(), item_id) for item_id in range(min, max + extra + 1)]
    shuffled_items.sort(key=lambda entry: entry[0])
    selected_items = []
    for _, item_id in shuffled_items:
        if str(item_id) in exclude or item_id > max:
            continue
        selected_items.append(item_id)
        if len(selected_items) >= how_many:
            break
    return selected_items
