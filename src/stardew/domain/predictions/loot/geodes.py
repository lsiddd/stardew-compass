"""Geodes rules adapted from MouseyPounds (MIT; predictor b9e7c71)."""

from ..report_support import (
    PredictionContext,
    SystemRandom,
    capture,
    compare_version,
    floor,
    set_slot,
)
from .seeds import player_sequence_seed
from .selection import append_object, set_object


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
        alternatives, opening_rules = _opening_results(
            save,
            items,
            item_ids,
            quantities,
            beans,
            trove_beans,
            hat,
            (5 if roll < 0.25 else 1) if modern else None,
        )
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
                    "dropAlternatives": alternatives[column],
                    "openingRule": opening_rules[column],
                },
            )


def _opening_results(
    save, items, item_ids, quantities, beans, trove_beans, hat, bean_quantity
):
    """Apply saved-state gates in the order of Utility and Clint's menu.

    Each column asks what opening this container at the selected counter would
    give with the saved flags. It does not simulate earlier hypothetical opens.
    """
    alternatives = [[] for _ in items]
    opening_rules = ["Clint; saved flags unchanged"] * len(items)

    def replace(column, item_id, name, quantity, rule):
        items[column], item_ids[column], quantities[column] = name, item_id, quantity
        opening_rules[column] = rule

    for column in range(len(items)):
        bean_roll = trove_beans if column >= 4 else beans
        if bean_roll:
            if save.get("qiCropsActive") and bean_quantity is not None:
                replace(
                    column,
                    "(O)890",
                    "Qi Bean",
                    bean_quantity,
                    "Active Qi crop challenge",
                )
            else:
                alternatives[column].append(
                    (
                        "Qi crop challenge active when opened",
                        "(O)890",
                        "Qi Bean",
                        bean_quantity,
                    )
                )
        if column == 5 and hat and item_ids[column] != "(O)890":
            has_hat = save.get("hasGoldenCoconutHat")
            if has_hat is False:
                replace(
                    column, "(H)75", "Golden Helmet", 1, "Golden Helmet not collected"
                )
            elif has_hat is None:
                alternatives[column].append(
                    (
                        "Golden Helmet not previously collected",
                        "(H)75",
                        "Golden Helmet",
                        1,
                    )
                )

        # This replacement belongs to GeodeMenu, outside the geode loot helper.
        object_data = save["objects"].get("_" + item_ids[column].removeprefix("(O)"))
        if column != 4 and object_data and object_data.get("type") == "Arch":
            found_artifact = save.get("hasArtifactFound")
            if found_artifact is False:
                replace(
                    column,
                    "(O)390",
                    "Stone",
                    5,
                    "No artifactFound mail received or pending",
                )
            elif found_artifact is None:
                alternatives[column].append(
                    ("No artifactFound mail received or pending", "(O)390", "Stone", 5)
                )

        # GeodeMenu bypasses Utility entirely for the first golden coconut.
        if column == 5:
            cracked = save.get("goldenCoconutCracked")
            if cracked is False:
                replace(
                    column, "(O)73", "Golden Walnut", 1, "First Golden Coconut at Clint"
                )
                alternatives[column].clear()
            elif cracked is None:
                alternatives[column].append(
                    (
                        "First Golden Coconut opened at Clint",
                        "(O)73",
                        "Golden Walnut",
                        1,
                    )
                )
    return alternatives, opening_rules


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
