"""Compatibility imports for the feature-local rules."""

from .features.bookseller import predict_bookseller
from .features.cart import predict_cart, predict_cart_1_6
from .features.krobus import predict_krobus
from .features.sandy import predict_sandy
from .features.shop_selection import (
    get_cart_item,
    get_random_items,
    get_random_wall_floor,
)
from .features.wallpaper import predict_wallpaper

__all__ = [
    "get_cart_item",
    "get_random_items",
    "get_random_wall_floor",
    "predict_bookseller",
    "predict_cart",
    "predict_cart_1_6",
    "predict_krobus",
    "predict_sandy",
    "predict_wallpaper",
]
