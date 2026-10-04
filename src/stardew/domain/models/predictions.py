"""Immutable result models shared by map predictions and renderers."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BubbleEvent:
    location: str
    x: int
    y: int
    start: int
    end: int | None
    kind: str


@dataclass(frozen=True, slots=True)
class DigItem:
    item_id: str
    name: str
    quantity: int
    runtime_dependent: bool = False
    alternatives: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ArtifactResult:
    location: str
    x: int
    y: int
    items: tuple[DigItem, ...]
    note: str | None
