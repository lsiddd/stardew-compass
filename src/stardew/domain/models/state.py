from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from collections.abc import Mapping, Iterator
from typing import Any
import re


def freeze(value: Any) -> Any:
    """Recursively freeze data, preserving insertion order of rule pools."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: freeze(child) for key, child in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(freeze(child) for child in value)
    if isinstance(value, set):
        return frozenset(value)
    return value


@dataclass(frozen=True, slots=True)
class SaveNode:
    """Lossless immutable saved fields; calculation code never sees XML nodes."""

    tag: str
    content: str | None = None
    attributes: Mapping[str, str] = field(default_factory=lambda: freeze({}))
    children: tuple[SaveNode, ...] = ()

    def __iter__(self) -> Iterator[SaveNode]:
        return iter(self.children)

    def __len__(self) -> int:
        return len(self.children)

    def get(self, key: str, default: str | None = None) -> str | None:
        return self.attributes.get(key, default)

    def text(self, default: str | None = None) -> str | None:
        return self.content if self.content is not None else default

    def iter(self, tag: str | None = None) -> Iterator[SaveNode]:
        if tag is None or tag == "*" or self.tag == tag:
            yield self
        for child in self.children:
            yield from child.iter(tag)

    def itertext(self) -> Iterator[str]:
        for node in self.iter():
            if node.content is not None:
                yield node.content

    def findall(self, path: str) -> tuple[SaveNode, ...]:
        if path in ("", "."):
            return (self,)
        path = path.removeprefix("./") if not path.startswith(".//") else path[1:]
        # Child and descendant axes, with the small saved-field predicate syntax.
        tokens = re.findall(r"//|/|(?:[^/\[]|\[[^\]]*\])+", path)
        current: tuple[SaveNode, ...] = (self,)
        descendants = False
        for token in tokens:
            if token == "//":
                descendants = True
                continue
            if token in ("/", "", "."):
                continue
            match = re.fullmatch(r"([^\[]+)(?:\[(.+)\])?", token)
            if match is None:
                raise ValueError(f"Unsupported saved-field path: {path}")
            tag, predicate = match.groups()
            found = []
            for node in current:
                candidates = (
                    (child for branch in node.children for child in branch.iter())
                    if descendants
                    else iter(node.children)
                )
                for child in candidates:
                    if tag != "*" and child.tag != tag:
                        continue
                    if predicate:
                        attr = re.fullmatch(r"@([^=]+)=['\"](.*)['\"]", predicate)
                        check = re.fullmatch(r"([^=]+)=['\"](.*)['\"]", predicate)
                        if attr and child.get(attr[1]) != attr[2]:
                            continue
                        if not attr and check and child.value(check[1]) != check[2]:
                            continue
                        if not attr and not check:
                            raise ValueError(
                                f"Unsupported saved-field predicate: {predicate}"
                            )
                    found.append(child)
            current, descendants = tuple(found), False
        return current

    def find(self, path: str) -> SaveNode | None:
        return next(iter(self.findall(path)), None)

    def value(self, path: str, default: str | None = None) -> str | None:
        node = self.find(path)
        return node.text(default) if node is not None else default

    findtext = value


def dictionary(node: SaveNode | None) -> Mapping[str, SaveNode]:
    if node is None:
        return freeze({})
    result = {}
    for entry in node.findall("item"):
        key, value = entry.find("key"), entry.find("value")
        if key is None or value is None:
            continue
        label = key.children[0].text() if key.children else key.text()
        if label is not None:
            result[label] = value
    return freeze(result)


@dataclass(frozen=True, slots=True)
class SaveMetadata:
    game_id: int
    game_version: str | None
    year: int | None
    season: str | None
    day: int | None
    days_played: int | None
    use_legacy_random: bool | None
    farm_type: int | None
    daily_luck: float | None


@dataclass(frozen=True, slots=True)
class ItemState:
    slot: int
    item_id: str | None
    name: str | None
    kind: str
    quantity: int | None
    quality: int | None
    is_recipe: bool | None
    big_craftable: bool | None
    attachments: tuple[ItemState, ...]
    enchantments: frozenset[str]
    snapshot: SaveNode = field(repr=False)


@dataclass(frozen=True, slots=True)
class PlayerState:
    name: str
    player_id: int | None
    farm_name: str | None
    stats: Mapping[str, int]
    inventory: tuple[ItemState, ...]
    equipment: Mapping[str, tuple[ItemState, ...]]
    experience: tuple[int, ...]
    skills: Mapping[str, int | None]
    mail: frozenset[str]
    collections: Mapping[str, Mapping[str, SaveNode]]
    relationships: Mapping[str, SaveNode]
    quests: tuple[SaveNode, ...]
    snapshot: SaveNode = field(repr=False)
    gender: str | None = None
    is_male: bool | None = None
    total_money_earned: int | None = None
    deepest_mine_level: int | None = None
    house_upgrade_level: int | None = None
    spouse: str | None = None
    has_special_charm: bool | None = None
    events: frozenset[str] = frozenset()
    achievements: frozenset[str] = frozenset()
    milliseconds_played: int | None = None
    use_separate_wallets: bool | None = None


@dataclass(frozen=True, slots=True)
class ContainerState:
    name: str
    location: str
    x: str | None
    y: str | None
    inventory: tuple[ItemState, ...]
    shared_inventory: str | None
    wallets: Mapping[str, tuple[ItemState, ...]]
    snapshot: SaveNode = field(repr=False)


@dataclass(frozen=True, slots=True)
class BuildingState:
    kind: str | None
    x: int | None
    y: int | None
    snapshot: SaveNode = field(repr=False)


@dataclass(frozen=True, slots=True)
class AnimalState:
    name: str | None
    kind: str | None
    age: int | None
    friendship: int | None
    happiness: int | None
    has_cracker: bool | None
    snapshot: SaveNode = field(repr=False)
    animal_id: int | None = None


@dataclass(frozen=True, slots=True)
class LocationState:
    name: str | None
    kind: str | None
    buildings: tuple[BuildingState, ...]
    snapshot: SaveNode = field(repr=False)
    museum_items: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class NpcState:
    name: str | None
    traits: frozenset[str]


@dataclass(frozen=True, slots=True)
class WorldState:
    containers: tuple[ContainerState, ...]
    shared_inventories: Mapping[str, tuple[ItemState, ...]]
    locations: tuple[LocationState, ...]
    animals: tuple[AnimalState, ...]
    special_orders: tuple[SaveNode, ...]
    snapshot: SaveNode = field(repr=False)
    npcs: tuple[NpcState, ...] = ()
    child_count: int = 0
    qi_crops_active: bool = False
    mines_difficulty: int | None = None
    times_fed_raccoons: int | None = None
    visits_until_y1_guarantee: int | None = None
    perfection_waivers: int | None = None
    applied_1_3_changes: bool | None = None
    applied_1_4_changes: bool | None = None
    treasure_totems_used: int | None = None
    lost_books_found: int | None = None
    golden_coconut_cracked: bool | None = None
    game_version_label: str | None = None


@dataclass(frozen=True, slots=True)
class GameState:
    source: Path
    metadata: SaveMetadata
    players: tuple[PlayerState, ...]
    world: WorldState
    snapshot: SaveNode = field(repr=False)

    @property
    def player(self) -> PlayerState:
        return self.players[0]

    @property
    def path(self) -> Path:
        return self.source

    @property
    def rules_version(self) -> str:
        """Resolve legacy rule versions while retaining missing saved metadata."""
        if self.metadata.game_version:
            return self.metadata.game_version
        if self.world.applied_1_4_changes:
            return "1.4"
        if self.world.applied_1_3_changes:
            return "1.3"
        return "1.2"
