"""Compiled paths for the immutable compatibility snapshot.

Only path syntax is cached. No cache retains saves or query results.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator
from functools import lru_cache
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from .state import SaveNode


class Step(NamedTuple):
    descendants: bool
    tag: str
    attribute: bool
    key: str | None
    expected: str | None


@lru_cache(maxsize=512)
def compile_path(path: str) -> tuple[Step, ...]:
    if path in ("", "."):
        return ()
    path = path[1:] if path.startswith(".//") else path.removeprefix("./")
    result = []
    descendants = False
    for token in re.findall(r"//|/|(?:[^/\[]|\[[^\]]*\])+", path):
        if token == "//":
            descendants = True
            continue
        if token in ("/", "", "."):
            continue
        match = re.fullmatch(r"([^\[]+)(?:\[(.+)\])?", token)
        if match is None:
            raise ValueError(f"Unsupported saved-field path: {path}")
        tag, predicate = match.groups()
        attribute, key, expected = False, None, None
        if predicate:
            check = re.fullmatch(r"(@?)([^=]+)=['\"](.*)['\"]", predicate)
            if check is None:
                raise ValueError(f"Unsupported saved-field predicate: {predicate}")
            prefix, key, expected = check.groups()
            attribute = bool(prefix)
        result.append(Step(descendants, tag, attribute, key, expected))
        descendants = False
    return tuple(result)


def select(nodes: Iterable[SaveNode], step: Step) -> Iterator[SaveNode]:
    for node in nodes:
        candidates = (
            (child for branch in node.children for child in branch.iter())
            if step.descendants
            else iter(node.children)
        )
        for child in candidates:
            if step.tag != "*" and child.tag != step.tag:
                continue
            if step.key is not None:
                actual = (
                    child.get(step.key) if step.attribute else child.value(step.key)
                )
                if actual != step.expected:
                    continue
            yield child
