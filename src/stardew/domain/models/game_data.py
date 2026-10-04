"""Loaded game data contracts independent of filesystem readers."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from stardew.domain.catalogs.items import ItemCatalog
from .maps import Map


@dataclass(frozen=True, slots=True)
class GameData:
    catalogs: Mapping[str, Any]
    items: ItemCatalog
    maps: Mapping[str, Map]
    artifact_tables: Mapping[str, Any]
    provenance: Mapping[str, Any]
