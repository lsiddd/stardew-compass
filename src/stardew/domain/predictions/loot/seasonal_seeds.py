"""Seasonal reward choices from Utility and Crop, without session RNG claims."""

RACCOON_SEEDS = (
    ("CarrotSeeds", "Carrot Seeds", "Spring days 1–23 or Winter days 21–28"),
    (
        "SummerSquashSeeds",
        "Summer Squash Seeds",
        "Summer days 1–20 or Spring days 24–28",
    ),
    ("BroccoliSeeds", "Broccoli Seeds", "Fall days 1–20 or Summer days 21–28"),
    ("PowdermelonSeeds", "Powdermelon Seeds", "Winter days 1–20 or Fall days 21–28"),
)
LOW_GRADE_SEEDS = (
    ("472", "473", "474", "475"),
    ("487", "483", "482", "484"),
    ("487", "488", "489", "490"),
)


def raccoon_seeds(day, quantity):
    """Return a dated result, or four bounded claim-date alternatives."""
    if day is not None:
        season, day_of_month = (day - 1) // 28 % 4, (day - 1) % 28 + 1
        if day_of_month > (23 if season == 0 else 20):
            season = (season + 1) % 4
        item_id, name, _ = RACCOON_SEEDS[season]
        return {"item_id": "(O)" + item_id, "name": name}, ()
    return None, tuple(
        (f"Date obtained: {condition}", "(O)" + item_id, name, quantity)
        for item_id, name, condition in RACCOON_SEEDS
    )


def low_grade_seeds(day, quantity, objects):
    """Crop.getRandomLowGradeCropForThisSeason uses unsaved Game1.random."""
    season = (day - 1) // 28 % 4 if day is not None else None
    pools = (LOW_GRADE_SEEDS[season],) if season in (0, 1, 2) else LOW_GRADE_SEEDS
    keys = tuple(dict.fromkeys(key for pool in pools for key in pool))
    condition = (
        "Session RNG, if opened on the saved date"
        if season in (0, 1, 2)
        else "Session RNG chooses Spring, Summer or Fall seeds in Winter; opening date otherwise unknown"
    )
    return tuple(
        (condition, "(O)" + key, objects["_" + key]["name"], quantity) for key in keys
    )
