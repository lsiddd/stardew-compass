import json
from pathlib import Path
import struct
import pytest
from stardew.infrastructure.xnb.reader import (
    Reader,
    read_xnb,
    unpack_xnb,
    type_name,
    float_json,
)

FIXTURES = Path(__file__).parents[1] / "fixtures"


def assert_ordered_equal(a, b):
    assert a == b
    if isinstance(a, dict):
        assert list(a) == list(b)
        for k in a:
            assert_ordered_equal(a[k], b[k])
    elif isinstance(a, list):
        for x, y in zip(a, b):
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
