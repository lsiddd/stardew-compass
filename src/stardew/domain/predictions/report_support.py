"""Native deterministic prediction calculations.

Rules adapted from MouseyPounds' MIT Stardew Predictor (b9e7c71).
Each function calculates facts in an isolated context; presentation never affects
random-number consumption. Item pool insertion order is preserved explicitly.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any
from math import floor, fmod as _fmod
import re
from stardew.domain.models import freeze
from stardew.domain.numeric import (
    SystemRandom,
    random_seed,
    hash_string,
    hash_array,
    int32,
    MAX,
    trunc_div,
    trunc_rem,
)


def fmod(left, right):
    value = _fmod(left, right)
    return int(value) if value.is_integer() else value


def deepcopy(value):
    """Copy immutable catalog pools into private working collections."""
    if isinstance(value, Mapping):
        return {str(key): deepcopy(child) for key, child in value.items()}
    if isinstance(value, (tuple, list)):
        return [deepcopy(child) for child in value]
    return value


def ordered_keys(pool):
    numeric = [
        key
        for key in pool
        if str(key).isdigit() and str(int(key)) == str(key) and (int(key) < 2**32 - 1)
    ]
    numeric.sort(key=int)
    return numeric + [key for key in pool if key not in numeric]


def set_slot(values, index, value):
    if isinstance(values, dict):
        values[str(index)] = value
        return
    index = int(index)
    if index >= len(values):
        values.extend([None] * (index + 1 - len(values)))
    values[index] = value


def remove_slice(values, index, count=1):
    removed = values[index : index + count]
    del values[index : index + count]
    return removed


def invalid_number(value):
    try:
        float(value)
    except (TypeError, ValueError):
        return True
    return value is None


def exact_seed_part(value):
    return trunc_rem(int(value), MAX)


def compare_version(a, b):

    def parts(v):
        fields = str(v).split(".")
        return tuple(
            (
                int(re.match("\\d+", field)[0]) if re.match("\\d+", field) else -1
                for field in fields[:3]
            )
        ) + (-1,) * max(0, 3 - len(fields))

    return (parts(a) > parts(b)) - (parts(a) < parts(b))


def immutable_fact(value):
    if isinstance(value, Mapping):
        return freeze(
            {
                str(key): immutable_fact(child)
                for key, child in value.items()
                if not isinstance(child, SystemRandom)
            }
        )
    if isinstance(value, (tuple, list)):
        return tuple((immutable_fact(child) for child in value))
    if isinstance(value, SystemRandom):
        return None
    return value


@dataclass(slots=True)
class PredictionContext:
    save: dict[str, Any]
    catalogs: Mapping[str, Any]
    player_index: int = 0
    count: int | None = None
    captures: list[tuple[str, dict[str, Any]]] = field(default_factory=list)
    day_range: tuple[int, int] | None = None


def capture(context, feature, facts):
    context.captures.append((feature, deepcopy(facts)))
