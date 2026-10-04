from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any
from .state import SaveMetadata, ItemState, ContainerState, AnimalState
from .predictions import ArtifactResult, BubbleEvent
from stardew.domain.progress.models import ProgressResult
from stardew.domain.predictions.report_models import (
    ReportPredictionOptions,
    PredictionSection,
)


@dataclass(frozen=True, slots=True)
class Diagnostic:
    feature: str
    message: str
    severity: str = "warning"


@dataclass(frozen=True, slots=True)
class ShippedItem:
    item_id: str
    name: str
    quantity: int


@dataclass(frozen=True, slots=True)
class ExtrasPlayer:
    name: str
    player_id: int | None
    inventory: tuple[ItemState, ...]
    equipment: Mapping[str, tuple[ItemState, ...]]
    experience: tuple[int, ...]
    skills: Mapping[str, int | None]
    shipped: tuple[ShippedItem, ...]


@dataclass(frozen=True, slots=True)
class ExtrasResult:
    players: tuple[ExtrasPlayer, ...]
    containers: tuple[ContainerState, ...]
    shared_inventories: Mapping[str, tuple[ItemState, ...]]
    rarecrows: tuple[str, ...]
    animals: tuple[AnimalState, ...]
    perfection_waivers: int | None


@dataclass(frozen=True, slots=True)
class AnalysisOptions:
    progress: tuple[str, ...] | None = None
    predictions: tuple[str, ...] | None = None
    extras: bool = True
    bubbles: bool = True
    artifacts: bool = True
    locations: tuple[str, ...] | None = None
    prediction_options: ReportPredictionOptions | None = None
    strict: bool = False

    def __post_init__(self) -> None:
        for name in ("progress", "predictions", "locations"):
            value = getattr(self, name)
            if value is not None:
                if isinstance(value, str):
                    raise TypeError(f"{name} must be a sequence of strings or None")
                sequence = tuple(value)
                if not all(isinstance(item, str) for item in sequence):
                    raise TypeError(f"{name} must be a sequence of strings or None")
                object.__setattr__(self, name, sequence)
        if isinstance(self.prediction_options, Mapping):
            object.__setattr__(
                self,
                "prediction_options",
                ReportPredictionOptions(**self.prediction_options),
            )
        elif self.prediction_options is not None and not isinstance(
            self.prediction_options, ReportPredictionOptions
        ):
            raise TypeError(
                "prediction_options must be ReportPredictionOptions or None"
            )


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    save_file: str
    metadata: SaveMetadata
    progress: tuple[ProgressResult, ...]
    predictions: tuple[PredictionSection, ...]
    bubbles: tuple[BubbleEvent, ...]
    artifacts: tuple[ArtifactResult, ...]
    extras: ExtrasResult | None
    diagnostics: tuple[Diagnostic, ...]
    provenance: Mapping[str, Any]
    schema_version: int = 2
