"""Read static map geometry and RGBA textures for plotting, without game assemblies.

The tBIN10 layout is interpreted from the installed xTile 1.6.15 reader.
Animations use their first frame; dynamic in-game map patches are not applied.
"""

from dataclasses import dataclass
from pathlib import Path
from .reader import Reader, unpack_xnb


def asset_reader(path, expected):
    reader = Reader(unpack_xnb(Path(path).read_bytes()))
    if reader.seven() != 1:
        raise ValueError(f"Unsupported graphics reader table: {path}")
    name, version = reader.string(), reader.unpack("i")
    if name.split(",", 1)[0] != expected or version != 0:
        raise ValueError(f"Unsupported graphics asset: {name}")
    if reader.seven() != 0 or reader.seven() != 1:
        raise ValueError("Invalid graphics root or shared resources.")
    return reader


def read_texture(path):
    from PIL import Image

    r = asset_reader(path, "Microsoft.Xna.Framework.Content.Texture2DReader")
    surface, width, height, levels = [r.unpack("i") for _ in range(4)]
    if surface != 0:
        raise ValueError(
            f"Unsupported texture surface format {surface}: {path}. Expected RGBA Color."
        )
    if not 0 < width <= 16384 or not 0 < height <= 16384 or not 1 <= levels <= 15:
        raise ValueError("Invalid texture dimensions or mipmap count.")
    pixels = None
    for level in range(levels):
        size = r.unpack("i")
        if size != max(1, width >> level) * max(1, height >> level) * 4:
            raise ValueError("Invalid RGBA texture length.")
        data = r.take(size)
        if level == 0:
            pixels = data
    if r.pos != len(r.data):
        raise ValueError("Trailing texture data.")
    # XNA stores premultiplied alpha; convert before normal alpha compositing.
    return Image.frombytes("RGBa", (width, height), pixels).convert("RGBA")


@dataclass
class TileSheet:
    source: str
    columns: int
    rows: int
    tile_width: int
    tile_height: int
    margin: tuple
    spacing: tuple


@dataclass
class Layer:
    name: str
    visible: bool
    width: int
    height: int
    tiles: list


@dataclass
class VisualMap:
    sheets: dict
    layers: list

    @property
    def width(self):
        return self.layers[0].width

    @property
    def height(self):
        return self.layers[0].height


class MapReader(Reader):
    def string(self):
        return self.take(self.unpack("i")).decode("utf-8")

    def size(self):
        return self.unpack("i"), self.unpack("i")

    def properties(self):
        values = {}
        for _ in range(self.count()):
            key, kind = self.string(), self.unpack("B")
            if kind == 0:
                value = bool(self.unpack("B"))
            elif kind == 1:
                value = self.unpack("i")
            elif kind == 2:
                value = self.unpack("f")
            elif kind == 3:
                value = self.string()
            else:
                raise ValueError(f"Unknown map property type: {kind}")
            values[key] = value
        return values

    def static_tile(self, sheet, sheets):
        index, blend = self.unpack("i"), self.unpack("B")
        self.properties()
        if (
            sheet not in sheets
            or not 0 <= index < sheets[sheet].columns * sheets[sheet].rows
        ):
            raise ValueError("Invalid map tile or tilesheet.")
        if blend not in (0, 1):
            raise ValueError("Unsupported map blend mode.")
        return sheet, index

    def animated_tile(self, sheets):
        self.unpack("i")  # frame interval
        count = self.count()
        if not count:
            raise ValueError("Animated tile has no frames.")
        sheet, first = None, None
        while count:
            tag = self.take(1)
            if tag == b"T":
                sheet = self.string()
            elif tag == b"S":
                tile = self.static_tile(sheet, sheets)
                if first is None:
                    first = tile
                count -= 1
            else:
                raise ValueError("Invalid animated map tile.")
        self.properties()
        return first

    def map(self):
        if self.take(6) != b"tBIN10":
            raise ValueError("Unsupported map format: expected tBIN10.")
        self.string()  # map ID
        self.string()  # description
        self.properties()
        sheets = {}
        for _ in range(self.count()):
            name = self.string()
            self.string()
            source = self.string()
            columns, rows = self.size()
            tw, th = self.size()
            margin, spacing = self.size(), self.size()
            self.properties()
            if (
                min(columns, rows, tw, th) <= 0
                or tw > 256
                or th > 256
                or name in sheets
            ):
                raise ValueError("Invalid map tilesheet.")
            sheets[name] = TileSheet(source, columns, rows, tw, th, margin, spacing)
        layers = []
        for _ in range(self.count()):
            name, visible = self.string(), bool(self.unpack("B"))
            self.string()
            width, height = self.size()
            self.size()  # logical tile dimensions (not the game's display zoom)
            self.properties()
            if not 0 < width <= 512 or not 0 < height <= 512:
                raise ValueError("Unsupported map dimensions.")
            tiles, sheet = [], None
            for y in range(height):
                end = (y + 1) * width
                while len(tiles) < end:
                    tag = self.take(1)
                    if tag == b"T":
                        sheet = self.string()
                    elif tag == b"N":
                        count = self.unpack("i")
                        if not 0 < count <= end - len(tiles):
                            raise ValueError("Invalid empty-tile run.")
                        tiles.extend([None] * count)
                    elif tag == b"S":
                        tiles.append(self.static_tile(sheet, sheets))
                    elif tag == b"A":
                        tiles.append(self.animated_tile(sheets))
                    else:
                        raise ValueError("Invalid map tile tag.")
            layers.append(Layer(name, visible, width, height, tiles))
        if not layers or self.pos != len(self.data):
            raise ValueError("Empty map or trailing map data.")
        return VisualMap(sheets, layers)


def read_visual_map(path):
    r = asset_reader(path, "xTile.Pipeline.TideReader")
    data = r.take(r.unpack("i"))
    if r.pos != len(r.data):
        raise ValueError("Trailing map asset data.")
    return MapReader(data).map()
