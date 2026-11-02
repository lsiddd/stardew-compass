import json
import struct
from pathlib import Path

import pytest

from stardew.infrastructure.xnb.reader import (
    Reader,
    float_json,
    read_xnb,
    type_name,
    unpack_xnb,
)

FIXTURES = Path(__file__).parents[1] / "fixtures"


def assert_ordered_equal(a, b):
    assert a == b
    if isinstance(a, dict):
        assert list(a) == list(b)
        for k in a:
            assert_ordered_equal(a[k], b[k])
    elif isinstance(a, list):
        for x, y in zip(a, b, strict=False):
            assert_ordered_equal(x, y)


@pytest.mark.parametrize("name", ["objects-synthetic", "locations-synthetic"])
def test_monogame_synthetic_schemas(name):
    assert_ordered_equal(
        read_xnb(FIXTURES / (name + ".xnb")),
        json.loads((FIXTURES / (name + ".json")).read_text()),
    )


@pytest.mark.parametrize("name", ["objects-synthetic", "locations-synthetic"])
def test_truncated_xnb_and_unknown_reader(name):
    data = (FIXTURES / (name + ".xnb")).read_bytes()
    for size in [0, 3, 9, 15, len(data) // 2, len(data) - 1]:
        with pytest.raises(ValueError):
            unpack_xnb(data[:size])
    payload = unpack_xnb(data)
    for size in [0, 3, 15, len(payload) // 2, len(payload) - 1]:
        with pytest.raises(ValueError):
            Reader(payload[:size]).read()
    with pytest.raises(ValueError, match="Unknown XNB"):
        Reader(payload.replace(b"ReflectiveReader", b"UnapprovedReader")).read()
    with pytest.raises(ValueError, match="Trailing XNB"):
        Reader(payload + b"x").read()


def test_invalid_header_and_varints():
    data = bytearray((FIXTURES / "objects-synthetic.xnb").read_bytes())
    for offset, value in [(0, 0), (3, ord("q")), (4, 4), (5, 64)]:
        bad = data[:]
        bad[offset] = value
        with pytest.raises(ValueError):
            unpack_xnb(bad)
    with pytest.raises(ValueError):
        Reader(b"\xff" * 5).seven()


def test_type_names_and_single_roundtrip():
    assert (
        type_name(
            "System.Collections.Generic.List`1[[System.Nullable`1[[System.Int32, mscorlib]], mscorlib]]"
        )
        == "System.Collections.Generic.List`1<System.Nullable`1<System.Int32>>"
    )
    assert float_json(struct.unpack("<f", struct.pack("<f", 0.1))[0]) == 0.1


def test_reject_different_game_schema_version():
    data = (FIXTURES / "objects-synthetic.xnb").read_bytes()
    with pytest.raises(ValueError, match="schema version"):
        Reader(unpack_xnb(data.replace(b"1.6.15.24356", b"1.6.16.24356"))).read()


def test_prediction_table_arrays_preserve_nulls_and_order():
    from stardew.infrastructure.xnb.reader import reader_type

    name = reader_type(
        "Microsoft.Xna.Framework.Content.ArrayReader`1[[System.String, mscorlib]]"
    )
    assert name == "System.String[]"
    reader = Reader(struct.pack("<i", 3) + b"\x01\x05first\x00\x01\x04last")
    reader.readers = ["System.String"]
    assert reader.raw(name) == ["first", None, "last"]
    with pytest.raises(ValueError, match="count"):
        Reader(struct.pack("<i", -1)).raw(name)


@pytest.mark.parametrize(
    "name,owner_type", [("Any", 1), ("AnyOrNone", 2), ("None", 3), ("Clint", 0)]
)
def test_shop_owner_calculated_fields(name, owner_type):
    # Explicit ContentSerializer field order from GameData.ShopOwnerData.
    payload = b"\x00\x01" + bytes([len(name)]) + name.encode() + b"\x00" * 5
    reader = Reader(payload)
    reader.readers = ["System.String"]
    result = reader.raw("StardewValley.GameData.Shops.ShopOwnerData")
    assert (result["Id"], result["Name"], result["Type"]) == (name, name, owner_type)
    assert reader.pos == len(payload)
