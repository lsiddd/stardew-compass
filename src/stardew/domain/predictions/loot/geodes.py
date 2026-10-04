"""Geodes rules adapted from MouseyPounds (MIT; predictor b9e7c71)."""

from ..report_support import (
    PredictionContext,
    SystemRandom,
    capture,
    compare_version,
    floor,
    set_slot,
)
from .selection import append_object, set_object
from .seeds import player_sequence_seed


def predict_geodes(
    context: PredictionContext, is_search: bool | None = None, offset: int | None = None
) -> None:
    """Calculate each geode type from the same sequence of random draws."""
    save = context.save
    page_size = context.count or 20
    player = context.player_index
    has_troves = compare_version(save["version"], "1.4") >= 0
    has_coconuts = compare_version(save["version"], "1.5") >= 0
    modern = compare_version(save["version"], "1.6") >= 0
    columns = 4 + int(has_troves) + int(has_coconuts)
    if offset is None:
        offset = page_size * floor(save["geodesCracked"][player] / page_size)
    for sequence in range(offset + 1, offset + page_size + 1):
        items = ["Stone"] * 4
        item_ids = ["(O)390"] * 4
        quantities = [1] * 4
        seed = (
            player_sequence_seed(save, sequence, player)
            if modern
            else sequence + save["gameID"] / 2
        )
        rng, trove_rng = (SystemRandom(seed), SystemRandom(seed))
        beans, trove_beans, hat = _trove_contents(
            save, rng, trove_rng, has_troves, has_coconuts, items, item_ids, quantities
        )
        roll = rng.double()
        good = roll < 0.5 if modern else roll >= 0.5
        if good:
            _mineral_contents(save, rng, sequence, items, item_ids)
        else:
            _basic_contents(save, rng, items, item_ids, quantities)
        for column in range(columns):
            capture(
                context,
                "predictGeodes",
                {
                    "numCracked": sequence,
                    "whichPlayer": player,
                    "c": column,
                    "item": items,
                    "itemQty": quantities,
                    "couldBeBeans": beans,
                    "couldBeBeansTrove": trove_beans,
                    "couldBeHat": hat,
                    "itemIDs": item_ids,
                },
            )


def _trove_contents(
    save, rng, trove_rng, has_troves, has_coconuts, items, item_ids, quantities
):
    if not has_troves:
        return (None, None, False)
    for _ in range(2):
        amount = rng.next(1, 10)
        trove_rng.next()
        for _ in range(amount):
            rng.double()
            trove_rng.double()
    beans = trove_beans = False
    if has_coconuts:
        beans = rng.double() < 0.1
        trove_beans = trove_rng.double() < 0.1
    roll = trove_rng.double()
    contents = save["geodeContents"]["275"]
    append_object(save, items, item_ids, str(contents[floor(roll * len(contents))]))
    quantities.append(1)
    hat = False
    if has_coconuts:
        hat = roll < 0.05
        contents = save["geodeContents"]["791"]
        index = floor(trove_rng.double() * len(contents))
        append_object(save, items, item_ids, str(contents[index]))
        quantities.append(5 if index in (2, 3, 6) else 1)
    return (beans, trove_beans, hat)


def _mineral_contents(save, rng, num_cracked, item, item_ids):
    roll = rng.double()
    set_object(
        save,
        item,
        item_ids,
        0,
        str(
            save.get("geodeContents").get("535")[
                int(floor(roll * len(save.get("geodeContents").get("535"))))
            ]
        ),
    )
    set_object(
        save,
        item,
        item_ids,
        1,
        str(
            save.get("geodeContents").get("536")[
                int(floor(roll * len(save.get("geodeContents").get("536"))))
            ]
        ),
    )
    set_object(
        save,
        item,
        item_ids,
        2,
        str(
            save.get("geodeContents").get("537")[
                int(floor(roll * len(save.get("geodeContents").get("537"))))
            ]
        ),
    )
    if compare_version(save.get("version"), "1.6") >= 0:
        if roll < 0.008 and num_cracked > 15:
            set_object(save, item, item_ids, 3, "_74")
        else:
            set_object(
                save,
                item,
                item_ids,
                3,
                str(
                    save.get("geodeContents").get("749")[
                        int(floor(rng.next(len(save.get("geodeContents").get("749")))))
                    ]
                ),
            )
    elif rng.double() < 0.008 and num_cracked > 15:
        set_object(save, item, item_ids, 3, "_74")
    else:
        set_object(
            save,
            item,
            item_ids,
            3,
            str(
                save.get("geodeContents").get("749")[
                    int(floor(roll * len(save.get("geodeContents").get("749"))))
                ]
            ),
        )


def _basic_contents(save, rng, item, item_ids, item_qty):
    qty = rng.next(3) * 2 + 1
    if rng.double() < 0.1:
        qty = 10
    if rng.double() < 0.01:
        qty = 20
    if rng.double() < 0.5:
        c = rng.next(4)
        if c < 2:
            set_object(save, item, item_ids, 0, "_390")
            set_slot(item_qty, 0, qty)
            set_slot(item, 1, item[0])
            set_slot(item_ids, 1, item_ids[0])
            set_slot(item_qty, 1, qty)
            set_slot(item, 2, item[0])
            set_slot(item_ids, 2, item_ids[0])
            set_slot(item_qty, 2, qty)
            set_slot(item, 3, item[0])
            set_slot(item_ids, 3, item_ids[0])
            set_slot(item_qty, 3, qty)
        elif c == 2:
            set_object(save, item, item_ids, 0, "_330")
            set_slot(item_qty, 0, 1)
            set_slot(item, 1, item[0])
            set_slot(item_ids, 1, item_ids[0])
            set_slot(item, 2, item[0])
            set_slot(item_ids, 2, item_ids[0])
            set_slot(item, 3, item[0])
            set_slot(item_ids, 3, item_ids[0])
        else:
            set_object(save, item, item_ids, 0, "_86")
            set_slot(item_qty, 0, 1)
            set_object(save, item, item_ids, 1, "_84")
            set_object(save, item, item_ids, 2, "_82")
            set_object(
                save,
                item,
                item_ids,
                3,
                str(
                    f"_{(82 + rng.next(3) * 2 if compare_version(save.get('version'), '1.3') >= 0 else 82)}"
                ),
            )
    else:
        roll = rng.double()
        c = floor(roll * 3)
        if c == 0:
            set_object(save, item, item_ids, 0, "_378")
            set_slot(item_qty, 0, qty)
        elif c == 1:
            set_object(
                save,
                item,
                item_ids,
                0,
                str("_380" if save.get("deepestMineLevel") > 25 else "_378"),
            )
            set_slot(item_qty, 0, qty)
        else:
            set_object(save, item, item_ids, 0, "_382")
            set_slot(item_qty, 0, qty)
        c = floor(roll * 4)
        if c == 0:
            set_object(save, item, item_ids, 1, "_378")
            set_slot(item_qty, 1, qty)
        elif c == 1:
            set_object(save, item, item_ids, 1, "_380")
            set_slot(item_qty, 1, qty)
        elif c == 2:
            set_object(save, item, item_ids, 1, "_382")
            set_slot(item_qty, 1, qty)
        else:
            set_object(
                save,
                item,
                item_ids,
                1,
                str("_384" if save.get("deepestMineLevel") > 75 else "_380"),
            )
            set_slot(item_qty, 1, qty)
        c = floor(roll * 5)
        if c == 0:
            set_object(save, item, item_ids, 2, "_378")
            set_slot(item, 3, item[2])
            set_slot(item_ids, 3, item_ids[2])
            set_slot(item_qty, 2, qty)
            set_slot(item_qty, 3, item_qty[2])
        elif c == 1:
            set_object(save, item, item_ids, 2, "_380")
            set_slot(item, 3, item[2])
            set_slot(item_ids, 3, item_ids[2])
            set_slot(item_qty, 2, qty)
            set_slot(item_qty, 3, item_qty[2])
        elif c == 2:
            set_object(save, item, item_ids, 2, "_382")
            set_slot(item, 3, item[2])
            set_slot(item_ids, 3, item_ids[2])
            set_slot(item_qty, 2, qty)
            set_slot(item_qty, 3, item_qty[2])
        elif c == 3:
            set_object(save, item, item_ids, 2, "_384")
            set_slot(item, 3, item[2])
            set_slot(item_ids, 3, item_ids[2])
            set_slot(item_qty, 2, qty)
            set_slot(item_qty, 3, item_qty[2])
        else:
            set_object(save, item, item_ids, 2, "_386")
            set_slot(item, 3, item[2])
            set_slot(item_ids, 3, item_ids[2])
            set_slot(item_qty, 2, floor(qty / 2 + 1))
            set_slot(item_qty, 3, item_qty[2])
