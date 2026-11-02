"""Raccoons rules adapted from MouseyPounds (MIT; predictor b9e7c71)."""

from ..report_support import (
    PredictionContext,
    SystemRandom,
    capture,
    deepcopy,
    floor,
    fmod,
    random_seed,
    set_slot,
)
from .seasonal_seeds import raccoon_seeds


def predict_raccoon(
    context: PredictionContext, is_search: bool | None = None, offset: int | None = None
) -> None:
    save = context.save
    page_size = context.count or 10
    if offset is None:
        offset = page_size * floor(save.get("timesFedRaccoons") / page_size)
    g = 1
    while g <= page_size:
        table_row = offset + g
        times_fed = table_row - 1
        rng = []
        s = 0
        while s < 4:
            set_slot(
                rng,
                s,
                SystemRandom(
                    random_seed(
                        save.get("gameID"),
                        times_fed * 377,
                        legacy=save["useLegacyRandom"],
                    )
                ),
            )
            i = 0
            while i < 10:
                rng[int(s)].next()
                i += 1
            s += 1
        bundle_item = []
        bundle_qty = [1, 1, 1]
        is_long = [False, False, False]
        if times_fed < 5:
            which_bundle = fmod(times_fed, 5)
        else:
            which_bundle = rng[0].next(5)
            s = 1
            while s < 4:
                rng[int(s)].next()
                s += 1
        _request_contents(context, which_bundle, rng, bundle_item, bundle_qty, is_long)
        _reward_contents(save, table_row, bundle_item, bundle_qty)
        reward_alternatives = (
            raccoon_seeds(None, bundle_qty[2])[1]
            if bundle_item[2] == "Raccoon Seeds"
            else ()
        )
        i = 0
        capture(
            context,
            "predictRaccoon",
            {
                "tableRow": table_row,
                "timesFed": times_fed,
                "bundleItem": bundle_item,
                "bundleQty": bundle_qty,
                "isLong": is_long,
                "rewardAlternatives": reward_alternatives,
                **_saved_request_state(save, times_fed),
            },
        )
        g += 1
    return None


def _saved_request_state(save, times_fed):
    if "raccoonBundleSeason" not in save:
        return {}
    current = times_fed == save["timesFedRaccoons"]
    if not current:
        return {
            "requestState": "future"
            if times_fed > save["timesFedRaccoons"]
            else "past",
            "requestSeason": None,
            "deliveredSlots": (),
            "requestConditions": "Request season is fixed on first activation, advancing to the next season after day 21; future rows do not update the saved bundle",
        }
    season = save.get("raccoonBundleSeason")
    day = save.get("daysPlayed")
    last = save.get("raccoonLastCompletedDay")
    ready_day = last + 8 if times_fed and last is not None else None
    if season in (0, 1, 2, 3):
        status = "active"
        condition = (
            "Saved request season, even if the calendar season has since changed"
        )
    elif season == -1 and day is not None and (not times_fed or ready_day is not None):
        if ready_day is not None and day < ready_day:
            status = "cooldown"
            season = None
            condition = "Seven days must pass after the previous completion; season locks when the next request is activated"
        else:
            status = "ready_to_activate"
            season = ((day - 1) // 28 + ((day - 1) % 28 + 1 > 21)) % 4
            condition = "If activated on the saved day; delaying activation can change the request season"
    else:
        status = "unknown"
        season = None
        condition = "Saved request season or cooldown data is missing; seasonal choices remain conditional"
    return {
        "requestState": status,
        "requestSeason": season,
        "deliveredSlots": save.get("raccoonBundleComplete", ()),
        "availableAfterDay": ready_day,
        "requestConditions": condition,
    }


def _request_contents(context, which_bundle, rng, bundle_item, bundle_qty, is_long):
    save = context.save
    prev_roll = []
    match which_bundle:
        case 0:
            choice = ["_722", "_721", "_716", "_719", "_723", "_718", "_372"]
            set_slot(
                bundle_item,
                0,
                save.get("objects")
                .get(str(choice[int(rng[0].next(len(choice)))]))
                .get("name"),
            )
            s = 1
            while s < 4:
                rng[int(s)].next()
                s += 1
            set_slot(bundle_qty, 0, 5)
            choice = deepcopy(context.catalogs["predictor_raccoon_fish"])
            set_slot(bundle_item, 1, "")
            set_slot(bundle_qty, 1, 1)
            set_slot(is_long, 1, True)
            set_slot(bundle_item, 1, [])
            s = 0
            while s < 4:
                index = rng[int(s)].next(len(choice[int(s)]))
                set_slot(
                    bundle_item[1],
                    s,
                    f"Smoked {save.get('objects').get(str(choice[int(s)][int(index)])).get('name')}",
                )
                s += 1
        case 1:
            choice = deepcopy(context.catalogs["predictor_raccoon_dried_fruit"])
            set_slot(is_long, 0, True)
            set_slot(bundle_item, 0, [])
            s = 0
            while s < 4:
                index = rng[int(s)].next(len(choice[int(s)]))
                set_slot(
                    bundle_item[0],
                    s,
                    f"Dried {save.get('objects').get(str(choice[int(s)][int(index)])).get('name')}",
                )
                set_slot(prev_roll, s, index)
                s += 1
            set_slot(is_long, 1, True)
            set_slot(bundle_item, 1, [])
            s = 0
            while s < 4:
                index = prev_roll[int(s)]
                while (
                    choice[int(s)][int(index)] == choice[int(s)][int(prev_roll[int(s)])]
                ):
                    index = rng[int(s)].next(len(choice[int(s)]))
                set_slot(
                    bundle_item[1],
                    s,
                    f"{save.get('objects').get(str(choice[int(s)][int(index)])).get('name')} Jelly",
                )
                s += 1
        case 2:
            choice = [
                ["_422", "_404", "_257"],
                ["_422", "_404"],
                ["_422", "_404", "_281"],
                ["_422", "_404"],
            ]
            set_slot(is_long, 0, True)
            set_slot(bundle_item, 0, [])
            s = 0
            while s < 4:
                index = rng[int(s)].next(len(choice[int(s)]))
                set_slot(
                    bundle_item[0],
                    s,
                    f"Dried {save.get('objects').get(str(choice[int(s)][int(index)])).get('name')}",
                )
                set_slot(prev_roll, s, index)
                s += 1
            choice = ["Egg (Any)", "Cave Carrot", "White Algae"]
            set_slot(bundle_item, 1, choice[int(rng[0].next(len(choice)))])
            set_slot(bundle_qty, 1, 5)
        case 3:
            choice = deepcopy(context.catalogs["predictor_raccoon_vegetables"])
            set_slot(is_long, 0, True)
            set_slot(bundle_item, 0, [])
            s = 0
            while s < 4:
                index = rng[int(s)].next(len(choice[int(s)]))
                set_slot(
                    bundle_item[0],
                    s,
                    f"{save.get('objects').get(str(choice[int(s)][int(index)])).get('name')} Juice",
                )
                set_slot(prev_roll, s, index)
                s += 1
            set_slot(is_long, 1, True)
            set_slot(bundle_item, 1, [])
            s = 0
            while s < 4:
                index = prev_roll[int(s)]
                while (
                    choice[int(s)][int(index)] == choice[int(s)][int(prev_roll[int(s)])]
                ):
                    index = rng[int(s)].next(len(choice[int(s)]))
                set_slot(
                    bundle_item[1],
                    s,
                    f"Pickled {save.get('objects').get(str(choice[int(s)][int(index)])).get('name')}",
                )
                s += 1
        case 4:
            choice = [
                "Moss_10",
                "110_1",
                "168_5",
                "766_99",
                "767_20",
                "535_8",
                "536_5",
                "537_3",
                "393_4",
                "397_2",
                "684_20",
                "72_1",
                "68_3",
                "156_3",
            ]
            index = rng[0].next(len(choice))
            piece = choice[int(index)].split("_")
            set_slot(
                bundle_item, 0, save.get("objects").get(str(f"_{piece[0]}")).get("name")
            )
            set_slot(bundle_qty, 0, piece[1])
            set_slot(prev_roll, 0, index)
            while index == prev_roll[0]:
                index = rng[0].next(len(choice))
            piece = choice[int(index)].split("_")
            set_slot(
                bundle_item, 1, save.get("objects").get(str(f"_{piece[0]}")).get("name")
            )
            set_slot(bundle_qty, 1, piece[1])


def _reward_contents(save, table_row, bundle_item, bundle_qty):
    match table_row:
        case 1:
            set_slot(bundle_item, 2, "Raccoon Seeds")
            set_slot(bundle_qty, 2, 25)
        case 2:
            set_slot(bundle_item, 2, "Raccoon Journal")
        case 3:
            set_slot(bundle_item, 2, "Raccoon Hat")
        case 4:
            set_slot(bundle_item, 2, "Fairy Dust")
            set_slot(bundle_qty, 2, 5)
        case 5:
            set_slot(bundle_item, 2, "Jungle Tank")
        case _:
            rng = SystemRandom(
                random_seed(
                    save.get("gameID"), table_row * 377, legacy=save["useLegacyRandom"]
                )
            )
            i = 0
            while i < 10:
                rng.next()
                i += 1
            match rng.next(5):
                case 0:
                    set_slot(bundle_item, 2, "Fairy Dust")
                    set_slot(bundle_qty, 2, 7)
                case 1:
                    set_slot(bundle_item, 2, "Book Of Stars")
                case 2:
                    set_slot(bundle_item, 2, "Next unshipped item OR Mystery Box")
                    set_slot(bundle_qty, 2, "1 OR 5")
                case 3:
                    set_slot(bundle_item, 2, "Stardrop Tea")
                case 4:
                    set_slot(bundle_item, 2, "Raccoon Seeds")
                    set_slot(bundle_qty, 2, 25)
                case _:
                    set_slot(bundle_item, 2, "Mystery Box")
                    set_slot(bundle_qty, 2, 3)
