"""Shared scalar contracts. Compatibility arithmetic lives in ``numeric``."""

import math
import re
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True, slots=True, order=True)
class GameVersion:
    major: int
    minor: int
    patch: int = 0
    revision: int = 0

    @classmethod
    @lru_cache(maxsize=64)
    def parse(cls, value: str) -> "GameVersion":
        if not isinstance(value, str) or not re.fullmatch(
            r"[0-9]+(?:\.[0-9]+){1,3}", value.strip()
        ):
            raise ValueError(f"Invalid game version: {value!r}")
        parts = [int(part) for part in value.strip().split(".")]
        return cls(*(parts + [0] * (4 - len(parts))))

    @property
    def triple(self) -> tuple[int, int, int]:
        return self.major, self.minor, self.patch


def exact_number(
    value: str | int | float | None, default: int | float = 0
) -> int | float:
    """Preserve integer precision, including old serialized collection counters."""
    if value is None or value == "":
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, str) and re.fullmatch(r"[+-]?[0-9]+", value.strip()):
        return int(value)
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(parsed):
        raise ValueError(f"Expected a finite number, got {value!r}")
    return int(parsed) if parsed.is_integer() else parsed


def finite_number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} must be a finite number")
    try:
        finite = math.isfinite(value)
    except OverflowError as error:
        raise ValueError(f"{field} must be a finite number") from error
    if not finite:
        raise ValueError(f"{field} must be a finite number")
    return float(value)
