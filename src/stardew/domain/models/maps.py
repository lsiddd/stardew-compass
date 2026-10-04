"""Immutable map geometry used by prediction rules."""

from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any

from .state import freeze


@dataclass(frozen=True, slots=True, init=False)
class Map:
    width: int
    height: int
    name: str | None
    layers: Mapping[str, Mapping[str, Any]]
    tilesets: tuple[Mapping[str, Any], ...]

    def __init__(self, data: Mapping[str, Any]) -> None:
        layers: dict[str, Mapping[str, Any]] = {}
        for layer in data["layers"]:
            layers.setdefault(layer["name"], layer)
        for key, value in (
            ("width", data["width"]),
            ("height", data["height"]),
            ("name", data.get("Name")),
            ("layers", freeze(layers)),
            ("tilesets", freeze(data["tilesets"])),
        ):
            object.__setattr__(self, key, value)

    def index(self, x: int, y: int, layer: str) -> int:
        tiles = self.layers.get(layer)
        if tiles is None:
            return -1
        index = x + tiles["width"] * y
        if index < 0:
            raise IndexError("Negative tile index.")
        return tiles["data"][index] if index < len(tiles["data"]) else 0

    def tile(self, index: int) -> Mapping[str, Any] | None:
        previous = None
        for tileset in self.tilesets:
            if index > tileset["firstgid"]:
                previous = tileset
            else:
                break
        if previous:
            return next(
                (
                    t
                    for t in previous.get("tiles") or []
                    if t["id"] + previous["firstgid"] == index
                ),
                None,
            )
        return None

    def property(self, x: int, y: int, prop: str, layer: str = "Back") -> bool:
        if self.name == "Mountains" and prop == "NoFishing" and layer == "Back":
            return x in (47, 48) and y in (3, 4, 5)
        tile = self.tile(self.index(x, y, layer))
        return bool(
            tile and any(p["name"] == prop for p in tile.get("properties") or [])
        )

    def open_water(self, x: int, y: int) -> bool:
        return self.property(x, y, "Water") and self.index(x, y, "Buildings") not in (
            628,
            629,
            734,
            759,
        )

    def distance_to_land(self, x: int, y: int) -> int:
        # Preserve the original border exclusion and final width increment.
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
                    0 < px < self.width
                    and 0 < py < self.height
                    and not self.property(px, py, "Water")
                ):
                    return radius - 1 if radius < 5 else 5
        return 5
