"""Name and ID selection without consuming random values or reordering pools."""

from collections.abc import Mapping
from typing import Any
from ..report_support import set_slot


def set_object(
    save: Mapping[str, Any],
    items: list[str],
    item_ids: list[str | None],
    column: int,
    raw_id: str,
) -> None:
    set_slot(items, column, save["objects"][raw_id]["name"])
    set_slot(item_ids, column, "(O)" + str(raw_id).removeprefix("_"))


def append_object(
    save: Mapping[str, Any], items: list[str], item_ids: list[str | None], raw_id: str
) -> None:
    items.append(save["objects"][raw_id]["name"])
    item_ids.append("(O)" + str(raw_id).removeprefix("_"))
