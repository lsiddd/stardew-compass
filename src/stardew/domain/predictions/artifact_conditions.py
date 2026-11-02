"""Validated artifact predicates; evaluation retains source order and RNG draws."""

import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from stardew.domain.values import finite_number


@dataclass(frozen=True, slots=True)
class Clause:
    key: str
    arguments: tuple[str, ...]
    negate: bool


ARITIES = {
    "PLAYER_LOCATION_NAME": 2,
    "LOCATION_SEASON": 2,
    "RANDOM": 1,
    "DAYS_PLAYED": 1,
    "PLAYER_HAS_MAIL": 2,
    "PLAYER_SPECIAL_ORDER_ACTIVE": 2,
    "PLAYER_SPECIAL_ORDER_RULE_ACTIVE": 2,
    "IS_ISLAND_NORTH_BRIDGE_FIXED": 0,
    "PLAYER_LUCK_LEVEL": 2,
    "PLAYER_MINING_LEVEL": 2,
}


@lru_cache(maxsize=512)
def compile_condition(expression: str | None) -> tuple[Clause, ...]:
    if expression is None or expression == "":
        return ()
    if not isinstance(expression, str):
        raise ValueError("Condition must be text or null")
    clauses = []
    for raw in expression.split(","):
        text = raw.strip()
        negate = text.startswith("!")
        parts = (text[1:] if negate else text).split()
        if parts:
            parts[0] = parts[0].upper()
        if not parts or parts[0] not in ARITIES or len(parts) != ARITIES[parts[0]] + 1:
            raise ValueError(f"Unsupported condition or argument count: {raw}")
        key, args = parts[0], tuple(parts[1:])
        if key.startswith("PLAYER_") and args[0].casefold() not in {
            "current",
            "target",
            "host",
        }:
            raise ValueError(f"Unsupported player selector: {raw}")
        if key == "LOCATION_SEASON" and args[0].casefold() not in {"here", "target"}:
            raise ValueError(f"Unsupported location selector: {raw}")
        if key == "RANDOM":
            probability = float(args[0])
            if not math.isfinite(probability) or not 0 <= probability <= 1:
                raise ValueError(f"Invalid condition probability: {raw}")
        if key in ("DAYS_PLAYED", "PLAYER_LUCK_LEVEL", "PLAYER_MINING_LEVEL"):
            int(args[-1])
        clauses.append(Clause(key, args, negate))
    return tuple(clauses)


def validate_artifact_tables(tables: Mapping[str, Any]) -> None:
    for name in ("Locations", "Objects", "ObjectNames"):
        if not isinstance(tables.get(name), Mapping) or not tables[name]:
            raise ValueError(f"{name}: expected a nonempty object")
    for identifier, item in tables["Objects"].items():
        if not isinstance(item, Mapping):
            raise ValueError(f"Objects/{identifier}: expected an object")
        for key in ("Name", "DisplayName", "Type"):
            if item.get(key) is not None and not isinstance(item[key], str):
                raise ValueError(f"Objects/{identifier}/{key}: expected text or null")
        chances = item.get("ArtifactSpotChances")
        if chances is not None:
            if not isinstance(chances, Mapping):
                raise ValueError(
                    f"Objects/{identifier}/ArtifactSpotChances: expected an object"
                )
            for chance in chances.values():
                if (
                    isinstance(chance, bool)
                    or not isinstance(chance, (int, float))
                    or not 0 <= chance <= 1
                ):
                    raise ValueError(
                        f"Objects/{identifier}/ArtifactSpotChances: invalid probability"
                    )
    if any(not isinstance(value, str) for value in tables["ObjectNames"].values()):
        raise ValueError("ObjectNames: expected string values")
    if "Default" not in tables["Locations"]:
        raise ValueError("Locations/Default: required artifact drop table missing")
    for name, location in tables["Locations"].items():
        if not isinstance(location, Mapping):
            raise ValueError(f"Locations/{name}: expected an object")
        drops = location.get("ArtifactSpots")
        if not isinstance(drops, (tuple, list)):
            raise ValueError(f"Locations/{name}/ArtifactSpots: expected an array")
        for index, drop in enumerate(drops):
            where = f"Locations/{name}/ArtifactSpots/{index}"
            try:
                if not isinstance(drop, Mapping):
                    raise ValueError("expected an object")
                for key in ("Precedence", "MinStack", "MaxStack"):
                    if isinstance(drop.get(key), bool) or not isinstance(
                        drop.get(key), int
                    ):
                        raise ValueError(f"{key}: expected an integer")
                chance = drop.get("Chance")
                if (
                    isinstance(chance, bool)
                    or not isinstance(chance, (int, float))
                    or not 0 <= chance <= 1
                ):
                    raise ValueError("Chance: expected a probability")
                for key in ("ApplyGenerousEnchantment", "ContinueOnDrop"):
                    if not isinstance(drop.get(key), bool):
                        raise ValueError(f"{key}: expected a Boolean")
                for key in ("RandomItemId", "StackModifiers"):
                    if key not in drop:
                        raise ValueError(f"{key}: required field missing")
                compile_condition(drop.get("Condition"))
                choices = drop.get("RandomItemId")
                if choices is not None and (
                    not isinstance(choices, (tuple, list))
                    or any(not isinstance(choice, str) for choice in choices)
                ):
                    raise ValueError(
                        "RandomItemId: expected an array of strings or null"
                    )
                if not choices and not isinstance(drop.get("ItemId"), str):
                    raise ValueError("ItemId: expected an item query")
                for query in choices or (drop["ItemId"],):
                    fallback = query.removeprefix("LOST_BOOK_OR_ITEM ").removeprefix(
                        "SECRET_NOTE_OR_ITEM "
                    )
                    if query != "RANDOM_ARTIFACT_FOR_DIG_SPOT" and not re.fullmatch(
                        r"\([A-Za-z]+\)\S+", fallback
                    ):
                        raise ValueError(f"unsupported item query: {query}")
                modifiers = drop.get("StackModifiers")
                if modifiers is not None and not isinstance(modifiers, (tuple, list)):
                    raise ValueError("StackModifiers: expected an array or null")
                for modifier in modifiers or ():
                    if (
                        not isinstance(modifier, Mapping)
                        or isinstance(modifier.get("Modification"), bool)
                        or modifier.get("Modification") != 0
                    ):
                        raise ValueError("unsupported stack modifier")
                    amount = modifier.get("Amount")
                    finite_number(amount, "stack modifier Amount")
                    compile_condition(modifier.get("Condition"))
            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(f"{where}: {error}") from error
