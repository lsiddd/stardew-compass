import struct
import pytest
from stardew.infrastructure.xnb.graphics import MapReader, read_texture, read_visual_map


def string7(text):
    data = text.encode()
    size, prefix = len(data), bytearray()
    while size >= 128:
        prefix.append((size & 127) | 128)
        size >>= 7
    prefix.append(size)
    return bytes(prefix) + data


def asset(name, data):
    payload = b"\1" + string7(name) + bytes(4) + b"\0\1" + data
    return b"XNBw\5\0" + struct.pack("<i", len(payload) + 10) + payload


def string(text):
    data = text.encode()
    return struct.pack("<i", len(data)) + data


def integer(value):
    return struct.pack("<i", value)


def map_bytes():
    # 2x1: one static tile and a two-frame animation (first frame is blue).
    sheet = (
        string("sheet")
        + string("")
        + string("synthetic")
        + struct.pack("<8i", 2, 1, 16, 16, 0, 0, 0, 0)
        + integer(0)
    )
    static = integer(0) + b"\0" + integer(0)
    blue = integer(1) + b"\0" + integer(0)
    animated = (
        integer(100)
        + integer(2)
        + b"T"
        + string("sheet")
        + b"S"
        + blue
        + b"S"
        + static
        + integer(0)
    )
    layer = (
        string("Back")
        + b"\1"
        + string("")
        + struct.pack("<4i", 2, 1, 16, 16)
        + integer(0)
        + b"T"
        + string("sheet")
        + b"S"
        + static
        + b"A"
        + animated
    )
    return (
        b"tBIN10"
        + string("")
        + string("")
        + integer(0)
        + integer(1)
        + sheet
        + integer(1)
        + layer
    )


def test_map_static_and_animated_tiles(tmp_path):
    data = map_bytes()
    path = tmp_path / "map.xnb"
    path.write_bytes(
        asset("xTile.Pipeline.TideReader, xTile", integer(len(data)) + data)
    )
    visual = read_visual_map(path)
    assert (visual.width, visual.height) == (2, 1)
    assert visual.layers[0].tiles == [("sheet", 0), ("sheet", 1)]
    assert visual.sheets["sheet"].source == "synthetic"
    for cut in (0, 6, len(data) // 2, len(data) - 1):
        with pytest.raises(ValueError):
            MapReader(data[:cut]).map()


def test_texture_premultiplied_alpha_and_rejected_formats(tmp_path):
    path = tmp_path / "texture.xnb"
    header = struct.pack("<5i", 0, 1, 1, 1, 4)
    path.write_bytes(
        asset(
            "Microsoft.Xna.Framework.Content.Texture2DReader",
            header + bytes([64, 0, 0, 128]),
        )
    )
    image = read_texture(path)
    assert image.mode == "RGBA"
    assert image.getpixel((0, 0)) == (127, 0, 0, 128)
    path.write_bytes(
        asset(
            "Microsoft.Xna.Framework.Content.Texture2DReader",
            struct.pack("<5i", 4, 1, 1, 1, 4) + bytes(4),
        )
    )
    with pytest.raises(ValueError, match="surface format"):
        read_texture(path)
    path.write_bytes(
        asset("Microsoft.Xna.Framework.Content.Texture2DReader", header + bytes(3))
    )
    with pytest.raises(ValueError, match="Truncated"):
        read_texture(path)


def test_invalid_map_header_and_property_type():
    with pytest.raises(ValueError, match="format"):
        MapReader(b"wrong!").map()
    with pytest.raises(ValueError, match="property type"):
        MapReader(integer(1) + string("property") + b"\xff").properties()


def test_empty_tile_runs():
    data = (
        b"tBIN10"
        + string("")
        + string("")
        + integer(0)
        + integer(0)
        + integer(1)
        + string("Back")
        + b"\1"
        + string("")
        + struct.pack("<4i", 2, 1, 16, 16)
        + integer(0)
    )
    assert MapReader(data + b"N" + integer(2)).map().layers[0].tiles == [None, None]
    with pytest.raises(ValueError, match="empty-tile run"):
        MapReader(data + b"N" + integer(3)).map()
