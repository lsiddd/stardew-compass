"""Bookseller rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    deepcopy,
    floor,
    fmod,
    hash_string,
    random_seed,
    remove_slice,
    trunc_div,
)


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
        case 1:
            possible_days = [9, 12, 18, 25, 27]
        case 2:
            possible_days = [4, 7, 8, 9, 12, 19, 22, 25]
        case 3:
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
    stock = {}
    d = 0
    while d < len(days):
        days_played = offset + days[int(d)] + save.get("dayAdjust")
        stock[str(d)] = {}
        rng = SystemRandom(
            random_seed(
                days_played,
                trunc_div(save["gameID"], 2),
                legacy=save["useLegacyRandom"],
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
    return None
