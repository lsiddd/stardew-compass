"""Schema v2 serializes facts, without XML, HTML or text bodies."""

from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any
import json
from stardew.domain.models.results import AnalysisResult


def to_data(value: Any) -> Any:
    if is_dataclass(value):
        return {
            field.name: to_data(getattr(value, field.name))
            for field in fields(value)
            if field.name != "snapshot"
        }
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
