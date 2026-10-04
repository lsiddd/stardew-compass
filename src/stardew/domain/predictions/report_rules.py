"""Calculation entry points shared by the structured prediction analysis."""

from .report_support import (
    PredictionContext,
    deepcopy,
    immutable_fact,
    compare_version,
    SystemRandom,
)
from .report_calendar import (
    get_random_item_from_season,
    predict_crane,
    predict_green_rain,
    predict_mines,
    predict_night,
    predict_statues,
    predict_trains,
    predict_trash,
)
from .report_shops import (
    get_cart_item,
    get_random_items,
    get_random_wall_floor,
    predict_bookseller,
    predict_cart,
    predict_cart_1_6,
    predict_krobus,
    predict_sandy,
    predict_wallpaper,
)
from .report_loot import (
    predict_enchantments,
    predict_geodes,
    predict_mystery_boxes,
    predict_prize_ticket,
    predict_raccoon,
)
from .report_events import (
    predict_calico_jack,
    predict_gem_birds,
    predict_makeover,
    predict_mine_chests,
    predict_winter_star,
)
