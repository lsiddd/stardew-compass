"""Public entry points: load once, inject data, calculate immutable results."""

from stardew.application import analyze
from stardew.domain.errors import FeatureUnavailable
from stardew.domain.models import GameState
from stardew.domain.models.game_data import GameData
from stardew.domain.models.results import AnalysisOptions, AnalysisResult
from stardew.domain.predictions.report_models import ReportPredictionOptions
from stardew.infrastructure.game_data import DataError, load_game_data
from stardew.infrastructure.saves import load_save

__all__ = [
    "load_save",
    "load_game_data",
    "analyze",
    "GameState",
    "GameData",
    "DataError",
    "AnalysisOptions",
    "AnalysisResult",
    "ReportPredictionOptions",
    "FeatureUnavailable",
]
