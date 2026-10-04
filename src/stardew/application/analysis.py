"""Coordinate typed calculations and feature-specific availability."""

from collections.abc import Callable, Mapping
from typing import Any, TypeVar

from stardew.domain.errors import FeatureUnavailable
from stardew.domain.models.state import GameState
from stardew.domain.models.game_data import GameData
from stardew.domain.models.results import AnalysisOptions, AnalysisResult, Diagnostic
from stardew.domain.models.predictions import ArtifactResult, BubbleEvent
from stardew.domain.progress.models import ProgressResult
from stardew.domain.predictions.report_models import PredictionSection
from .extras import analyze_extras


Result = TypeVar("Result")


def analyze(
    state: GameState,
    *,
    data: GameData,
    options: AnalysisOptions | Mapping[str, Any] | None = None,
) -> AnalysisResult:
    """Analyze selected features with shared, immutable saved state and game data."""
    if options is None:
        options = AnalysisOptions()
    elif isinstance(options, Mapping):
        options = AnalysisOptions(**options)
    if not isinstance(options, AnalysisOptions):
        raise TypeError("options must be AnalysisOptions or a mapping of its fields")
    diagnostics: list[Diagnostic] = []

    def feature(
        name: str, calculate: Callable[[], tuple[Result, ...]]
    ) -> tuple[Result, ...]:
        try:
            return calculate()
        except FeatureUnavailable as error:
            if options.strict:
                raise
            diagnostics.append(Diagnostic(name, str(error)))
            return ()

    progress: tuple[ProgressResult, ...] = ()
    predictions: tuple[PredictionSection, ...] = ()
    bubbles: tuple[BubbleEvent, ...] = ()
    artifacts: tuple[ArtifactResult, ...] = ()
    if options.progress != ():
        from stardew.domain.progress import analyze_progress

        progress = feature(
            "progress", lambda: analyze_progress(state, data, options.progress)
        )
    if options.predictions != ():
        from stardew.domain.predictions.report_predictions import analyze_predictions

        predictions = feature(
            "predictions",
            lambda: analyze_predictions(
                state, data, options.predictions, options.prediction_options
            ),
        )
    if options.bubbles:
        from stardew.domain.predictions.bubbles import predict_bubbles

        bubbles = feature(
            "bubbles", lambda: predict_bubbles(state, data, options.locations)
        )
    if options.artifacts:
        from stardew.domain.predictions.artifacts import predict_artifacts

        artifacts = feature(
            "artifacts", lambda: predict_artifacts(state, data, options.locations)
        )
    sections: tuple[ProgressResult | PredictionSection, ...] = (*progress, *predictions)
    for result in sections:
        if not result.available:
            notes = result.diagnostics
            if options.strict:
                raise FeatureUnavailable(
                    f"{result.section_id}: " + "; ".join(str(note) for note in notes)
                )
            for note in notes:
                diagnostics.append(Diagnostic(result.section_id, str(note)))
    return AnalysisResult(
        state.source.name,
        state.metadata,
        tuple(progress),
        tuple(predictions),
        tuple(bubbles),
        tuple(artifacts),
        analyze_extras(state, data) if options.extras else None,
        tuple(diagnostics),
        data.provenance,
    )
