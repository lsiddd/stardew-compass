"""Wallpaper rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    random_seed,
    trunc_div,
)
from .shop_selection import get_random_wall_floor


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
                    trunc_div(save["gameID"], 2),
                    legacy=save["useLegacyRandom"],
                )
            )
            rng_j = SystemRandom(
                random_seed(
                    day + save.get("dayAdjust"),
                    trunc_div(save["gameID"], 2),
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
