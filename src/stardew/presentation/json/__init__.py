"""Schema v2 serializes facts, without XML, HTML or text bodies."""

import json
from collections.abc import Mapping
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any

from stardew.domain.models.results import AnalysisResult

from .wire import WIRE_FIELDS


def to_data(value: Any) -> Any:
    if is_dataclass(value):
        names = WIRE_FIELDS.get(type(value))
        if names is None:
            raise TypeError(f"No public JSON contract for {type(value).__name__}")
        return {name: to_data(getattr(value, name)) for name in names}
    if isinstance(value, Mapping):
        return {str(key): to_data(child) for key, child in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_data(child) for child in value]
    if isinstance(value, (set, frozenset)):
        return [to_data(child) for child in sorted(value)]
    if isinstance(value, Path):
        return str(value)
    return value


def render_json(result: AnalysisResult) -> str:
    return (
        json.dumps(to_data(result), ensure_ascii=False, indent=2, allow_nan=False)
        + "\n"
    )
