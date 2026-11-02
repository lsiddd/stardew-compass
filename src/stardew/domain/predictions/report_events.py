"""Compatibility imports for the feature-local rules."""

from .features.calico_jack import predict_calico_jack
from .features.festival import predict_makeover
from .features.gem_birds import predict_gem_birds
from .features.mine_chests import predict_mine_chests
from .features.winter_star import predict_winter_star

__all__ = [
    "predict_calico_jack",
    "predict_gem_birds",
    "predict_makeover",
    "predict_mine_chests",
    "predict_winter_star",
]
