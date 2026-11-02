"""Compatibility imports for the feature-local rules."""

from .features.crane import predict_crane
from .features.mines import predict_mines
from .features.night import predict_night
from .features.statues import predict_statues
from .features.trains import predict_trains
from .features.trash import get_random_item_from_season, predict_trash
from .features.weather import predict_green_rain

__all__ = [
    "get_random_item_from_season",
    "predict_crane",
    "predict_green_rain",
    "predict_mines",
    "predict_night",
    "predict_statues",
    "predict_trains",
    "predict_trash",
]
