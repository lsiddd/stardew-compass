"""Immutable map geometry used by prediction rules."""

from bisect import bisect_right
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from .state import freeze


@dataclass(frozen=True, slots=True, init=False)
class Map:
    width: int
    height: int
    name: str | None
    layers: Mapping[str, Mapping[str, Any]]
    tilesets: tuple[Mapping[str, Any], ...]
    _tiles: Mapping[int, Mapping[str, Any]] = field(repr=False, compare=False)
    _properties: Mapping[int, frozenset[str]] = field(repr=False, compare=False)
    _first_gids: tuple[int, ...] = field(repr=False, compare=False)
    _cell_properties: Mapping[tuple[str, int, int], frozenset[str]] = field(
        repr=False, compare=False
    )

    def __init__(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            raise ValueError("expected a map object")
        for dimension in ("width", "height"):
            value = data.get(dimension)
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not 0 < value <= 512
            ):
                raise ValueError(f"{dimension} must be an integer between 1 and 512")
        if not isinstance(data.get("layers"), (list, tuple)) or not isinstance(
            data.get("tilesets"), (list, tuple)
        ):
            raise ValueError("layers and tilesets must be arrays")
        layers: dict[str, Mapping[str, Any]] = {}
        for layer in data["layers"]:
            if not isinstance(layer, Mapping) or not isinstance(layer.get("name"), str):
                raise ValueError("each layer needs a name")
            if layer["name"] in layers:
                continue  # The reference uses the first layer with each name.
            width, cells = layer.get("width"), layer.get("data")
            if (
                isinstance(width, bool)
                or not isinstance(width, int)
                or not 0 < width <= 512
            ):
                raise ValueError(f"layer {layer['name']}: invalid width")
            if (
                not isinstance(cells, (list, tuple))
                or len(cells) > 512 * 512
                or any(isinstance(v, bool) or not isinstance(v, int) for v in cells)
            ):
                raise ValueError(f"layer {layer['name']}: invalid tile data")
            layers.setdefault(layer["name"], layer)
        previous_gid = -1
        for tileset in data["tilesets"]:
            first = tileset.get("firstgid") if isinstance(tileset, Mapping) else None
            if (
                isinstance(first, bool)
                or not isinstance(first, int)
                or first < max(0, previous_gid)
            ):
                raise ValueError("tilesets must have ordered integer firstgid values")
            previous_gid = first
        for key, value in (
            ("width", data["width"]),
            ("height", data["height"]),
            ("name", data.get("Name")),
            ("layers", freeze(layers)),
            ("tilesets", freeze(data["tilesets"])),
        ):
            object.__setattr__(self, key, value)
        tiles: dict[int, Mapping[str, Any]] = {}
        for position, tileset in enumerate(self.tilesets):
            upper = (
                self.tilesets[position + 1]["firstgid"]
                if position + 1 < len(self.tilesets)
                else float("inf")
            )
            for tile in tileset.get("tiles") or ():
                identifier = tile.get("id") if isinstance(tile, Mapping) else None
                if (
                    isinstance(identifier, bool)
                    or not isinstance(identifier, int)
                    or identifier < 0
                ):
                    raise ValueError("tile id must be an integer")
                props = tile.get("properties") or ()
                if not isinstance(props, (list, tuple)) or any(
                    not isinstance(p, Mapping) or not isinstance(p.get("name"), str)
                    for p in props
                ):
                    raise ValueError("tile properties must have names")
                gid = identifier + tileset["firstgid"]
                if tileset["firstgid"] <= gid < upper:
                    tiles.setdefault(gid, tile)
        object.__setattr__(self, "_tiles", freeze(tiles))
        object.__setattr__(
            self, "_first_gids", tuple(t["firstgid"] for t in self.tilesets)
        )
        cells = {}
        for cell in data.get("tile_properties", ()):
            if not isinstance(cell, Mapping):
                raise ValueError("tile properties must identify a tile")
            x, y, layer = cell.get("x"), cell.get("y"), cell.get("layer", "Back")
            if (
                isinstance(x, bool)
                or not isinstance(x, int)
                or isinstance(y, bool)
                or not isinstance(y, int)
                or not 0 <= x < self.width
                or not 0 <= y < self.height
                or layer not in layers
            ):
                raise ValueError("tile property coordinates must be on a known layer")
            props = cell.get("properties")
            if not isinstance(props, (list, tuple)) or any(
                not isinstance(p, Mapping) or not isinstance(p.get("name"), str)
                for p in props
            ):
                raise ValueError("tile properties must have names")
            cells[(layer, x, y)] = frozenset(p["name"] for p in props)
        object.__setattr__(self, "_cell_properties", freeze(cells))
        object.__setattr__(
            self,
            "_properties",
            freeze(
                {
                    gid: frozenset(p["name"] for p in tile.get("properties") or ())
                    for gid, tile in tiles.items()
                }
            ),
        )

    def index(self, x: int, y: int, layer: str) -> int:
        tiles = self.layers.get(layer)
        if tiles is None:
            return -1
        if x < 0 or y < 0:
            raise IndexError("Negative tile index.")
        if x >= tiles["width"] or y >= self.height:
            return 0
        index = x + tiles["width"] * y
        return tiles["data"][index] if index < len(tiles["data"]) else 0

    def tile(self, index: int) -> Mapping[str, Any] | None:
        return self._tiles.get(index)

    def property(self, x: int, y: int, prop: str, layer: str = "Back") -> bool:
        return prop in self._cell_properties.get((layer, x, y), ()) or prop in (
            self._properties.get(self.index(x, y, layer), ())
        )

    def tile_index(self, x: int, y: int, layer: str, tilesheet: str) -> int:
        """Resolve a global map ID to a local index on the selected tilesheet."""
        gid = self.index(x, y, layer)
        position = bisect_right(self._first_gids, gid) - 1
        if gid <= 0 or position < 0:
            return -1
        source = self.tilesets[position]
        return gid - source["firstgid"] if source.get("name") == tilesheet else -1

    def open_water(self, x: int, y: int) -> bool:
        return self.property(x, y, "Water") and self.tile_index(
            x, y, "Buildings", "outdoors"
        ) not in (
            628,
            629,
            734,
            759,
        )

    def distance_to_land(self, x: int, y: int) -> int:
        # The game's final width increment makes radius 5 return 5, not 4.
        for radius in range(1, 6):
            sx, sy, ex, ey = x - radius, y - radius, x + radius + 1, y + radius + 1
            perimeter = (
                [(i, sy) for i in range(sx, ex)]
                + [(ex - 1, i) for i in range(sy + 1, ey)]
                + [(i, ey - 1) for i in range(ex - 2, sx - 1, -1)]
                + [(sx, i) for i in range(ey - 2, sy, -1)]
            )
            for px, py in perimeter:
                if (
                    0 <= px < self.width
                    and 0 <= py < self.height
                    and not self.property(px, py, "Water")
                ):
                    return radius - 1 if radius < 5 else 5
        return 5
