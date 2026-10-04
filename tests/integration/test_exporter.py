import json
import struct
from pathlib import Path
import pytest
from stardew.infrastructure.xnb.exporter import export

FIXTURES = Path(__file__).parents[1] / "fixtures"


def string_table():
    def seven(value):
        out = bytearray()
        while value >= 128:
            out.append((value & 127) | 128)
            value >>= 7
        out.append(value)
        return out

    def string(value):
        value = value.encode("utf-8")
        return seven(len(value)) + value

    prefix = "Microsoft.Xna.Framework.Content."
    readers = [
        prefix
        + "DictionaryReader`2[[System.String, mscorlib],[System.String, mscorlib]]",
        prefix + "StringReader",
    ]
    payload = (
        seven(2)
        + b"".join(string(r) + bytes(4) for r in readers)
        + b"\x00\x01"
        + struct.pack("<i", 1)
        + b"\x02"
        + string("synthetic")
        + b"\x02"
        + string("Português")
    )
    return b"XNBw\x05\x00" + struct.pack("<i", len(payload) + 10) + payload


def test_export_validates_every_input_before_writing(tmp_path):
    game, output = tmp_path / "game", tmp_path / "out"
    (game / "Content/Data").mkdir(parents=True)
    (game / "Content/Strings").mkdir()
    (game / "Stardew Valley.dll").write_bytes(b"synthetic source hash only")
    (game / "Content/Data/Objects.xnb").write_bytes(
        (FIXTURES / "objects-synthetic.xnb").read_bytes()
    )
    (game / "Content/Data/Locations.xnb").write_bytes(
        (FIXTURES / "locations-synthetic.xnb").read_bytes()
    )
    (game / "Content/Strings/Objects.pt-BR.xnb").write_bytes(b"truncated")
    with pytest.raises(ValueError):
        export(game, output)
    assert not output.exists()
    output.mkdir()
    (output / "Objects.json").write_text("previous valid table")
    with pytest.raises(ValueError):
        export(game, output)
    assert (output / "Objects.json").read_text() == "previous valid table"
    with pytest.raises(ValueError, match="outside"):
        export(game, game / "out")


def test_successful_synthetic_export_and_source_hashes(tmp_path):
    import hashlib

    game, out = tmp_path / "game", tmp_path / "out"
    (game / "Content/Data").mkdir(parents=True)
    (game / "Content/Strings").mkdir()
    sources = {
        "Stardew Valley.dll": b"hashed only, never loaded",
        "Content/Data/Objects.xnb": (FIXTURES / "objects-synthetic.xnb").read_bytes(),
        "Content/Data/Locations.xnb": (
            FIXTURES / "locations-synthetic.xnb"
        ).read_bytes(),
        "Content/Strings/Objects.pt-BR.xnb": string_table(),
    }
    for name, data in sources.items():
        (game / name).write_bytes(data)
    export(game, out)
    assert json.loads((out / "ObjectNames.json").read_text()) == {
        "synthetic": "Português"
    }
    assert json.loads((out / "provenance.json").read_text()) == {
        "sources": {
            name: hashlib.sha256(data).hexdigest().upper()
            for name, data in sources.items()
        }
    }
    assert all((game / name).read_bytes() == data for name, data in sources.items())
    # A valid XNB with the wrong root type is still not a valid game table.
    (game / "Content/Data/Objects.xnb").write_bytes(string_table())
    with pytest.raises(ValueError, match="Incompatible XNB type"):
        export(game, out)


def test_export_refuses_symlink_before_replacing_any_table(tmp_path):
    game, out = tmp_path / "game", tmp_path / "out"
    (game / "Content/Data").mkdir(parents=True)
    (game / "Content/Strings").mkdir()
    (game / "Stardew Valley.dll").write_bytes(b"synthetic")
    for table in ("Objects", "Locations"):
        (game / "Content/Data" / f"{table}.xnb").write_bytes(
            (FIXTURES / (table.lower() + "-synthetic.xnb")).read_bytes()
        )
    (game / "Content/Strings/Objects.pt-BR.xnb").write_bytes(string_table())
    out.mkdir()
    (out / "Objects.json").write_text("previous table")
    target = tmp_path / "personal.json"
    target.write_text("personal data")
    (out / "Locations.json").symlink_to(target)
    with pytest.raises(ValueError, match="symbolic link"):
        export(game, out)
    assert (out / "Objects.json").read_text() == "previous table"
    assert target.read_text() == "personal data"
    assert not (out / "ObjectNames.json").exists()
