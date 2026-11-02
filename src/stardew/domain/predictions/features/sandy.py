"""Sandy rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    random_seed,
    trunc_div,
)
from .shop_selection import get_random_items


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
                    trunc_div(save["gameID"], 2),
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
