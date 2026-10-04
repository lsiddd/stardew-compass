"""Immutable facts returned by the deterministic report prediction rules."""

from dataclasses import dataclass
from typing import TypeAlias
from collections.abc import Mapping

FactValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | tuple["FactValue", ...]
    | Mapping[str, "FactValue"]
)


@dataclass(frozen=True, slots=True)
class ReportPredictionOptions:
    start: int | None = None
    count: int | None = None
    player_indices: tuple[int, ...] | None = None
    day_offset: int = 0
    daily_luck: float | None = None
    luck_level: int = 0
    item_filter: str | None = None
    game_start: int = 1

    def __post_init__(self) -> None:
        for name in ("start", "count", "day_offset", "luck_level", "game_start"):
            value = getattr(self, name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int)
            ):
                raise TypeError(f"{name} must be an integer")
        if self.player_indices is not None:
            indices = tuple(self.player_indices)
            if any(
                isinstance(index, bool) or not isinstance(index, int)
                for index in indices
            ):
                raise TypeError("player_indices must be a sequence of integers")
            object.__setattr__(self, "player_indices", indices)
        if self.game_start < 1:
            raise ValueError("Calico Jack game start must be positive.")
        if self.start is not None and self.start < 1:
            raise ValueError("Prediction start must be positive.")
        if self.count is not None and not 1 <= self.count <= 10000:
            raise ValueError("Prediction count must be between 1 and 10000.")


@dataclass(frozen=True, slots=True)
class PredictionDate:
    days_played: int
    year: int
    season: str
    day: int


@dataclass(frozen=True, slots=True)
class PredictionFact:
    name: str
    value: FactValue


@dataclass(frozen=True, slots=True)
class PredictionAlternative:
    condition: str
    item_id: str | None
    item_name: str
    quantity: int | None = None


@dataclass(frozen=True, slots=True)
class PredictionRecord:
    date: PredictionDate | None = None
    sequence: int | None = None
    player_id: int | None = None
    location: str | None = None
    time: int | None = None
    item_id: str | None = None
    item_name: str | None = None
    quantity: int | None = None
    price: int | None = None
    alternatives: tuple[PredictionAlternative, ...] = ()
    facts: tuple[PredictionFact, ...] = ()


@dataclass(frozen=True, slots=True)
class PredictionSection:
    section_id: str
    title: str
    records: tuple[PredictionRecord, ...]
    diagnostics: tuple[str, ...] = ()
    available: bool = True
