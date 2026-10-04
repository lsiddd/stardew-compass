"""Public entry points: load once, inject data, calculate immutable results."""

from stardew.infrastructure.saves import load_save
from stardew.infrastructure.game_data import load_game_data, DataError
from stardew.domain.models.game_data import GameData
from stardew.application import analyze
from stardew.domain.models import GameState
from stardew.domain.models.results import AnalysisOptions, AnalysisResult
from stardew.domain.predictions.report_models import ReportPredictionOptions
from stardew.domain.errors import FeatureUnavailable

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
