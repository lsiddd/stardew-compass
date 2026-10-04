"""Immutable facts produced by progress calculations."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ProgressItem:
    item_id: str
    name: str
    count: int | float | None = None
    goal: int | float | None = None
    missing: int | float | None = None
    category: str | None = None
    hint: str | None = None
    alternatives: tuple[str, ...] = ()
    quality: int | None = None
    cost: int | float | None = None
    cost_unit: str | None = None
    level: int | None = None
    next_goal: int | float | None = None
    next_missing: int | float | None = None
    hearts: int | float | None = None
    status: str | None = None
    event_ids: tuple[str, ...] = ()
    kind: str | None = None


@dataclass(frozen=True, slots=True)
class ProgressMetric:
    metric_id: str
    name: str
    count: int | float
    goal: int | float
    complete: bool
    percentage: float
    missing_ids: tuple[str, ...] = ()
    player_id: str | None = None
    weight: float | None = None
    earned: float | None = None
    possible: bool = True


@dataclass(frozen=True, slots=True)
class ProgressFact:
    name: str
    value: Any


@dataclass(frozen=True, slots=True)
class PlayerProgress:
    player_id: str
    name: str
    metrics: tuple[ProgressMetric, ...] = ()
    items: tuple[ProgressItem, ...] = ()
    facts: tuple[ProgressFact, ...] = ()


@dataclass(frozen=True, slots=True)
class ProgressResult:
    section_id: str
    title: str
    metrics: tuple[ProgressMetric, ...] = ()
    players: tuple[PlayerProgress, ...] = ()
    items: tuple[ProgressItem, ...] = ()
    facts: tuple[ProgressFact, ...] = ()
    available: bool = True
    diagnostics: tuple[str, ...] = ()


def metric(
    metric_id,
    name,
    count,
    goal,
    missing_ids=(),
    *,
    player_id=None,
    weight=None,
    possible=True,
):
    percentage = min(100.0, max(0.0, 100.0 * count / goal)) if goal else 0.0
    return ProgressMetric(
        metric_id,
        name,
        count,
        goal,
        goal > 0 and count >= goal,
        percentage,
        tuple(str(x) for x in missing_ids),
        player_id,
        weight,
        percentage * weight / 100 if weight is not None else None,
        possible,
    )


def facts(**values):
    return tuple(ProgressFact(name, value) for name, value in values.items())
