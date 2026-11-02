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
    assert (output / "Objects.json").read_text(
        encoding="utf-8"
    ) == "previous valid table"
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
    assert json.loads((out / "ObjectNames.json").read_text(encoding="utf-8")) == {
        "synthetic": "Português"
    }
    assert json.loads((out / "provenance.json").read_text(encoding="utf-8")) == {
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
    assert (out / "Objects.json").read_text(encoding="utf-8") == "previous table"
    assert target.read_text(encoding="utf-8") == "personal data"
    assert not (out / "ObjectNames.json").exists()


@pytest.mark.parametrize("prior_export", [False, True])
def test_interrupted_export_is_detected_by_manifest(
    tmp_path, monkeypatch, prior_export
):
    import os

    from stardew.api import load_game_data
    from stardew.infrastructure.data_files import DataError

    game, out = tmp_path / "game", tmp_path / "out"
    (game / "Content/Data").mkdir(parents=True)
    (game / "Content/Strings").mkdir()
    (game / "Stardew Valley.dll").write_bytes(b"synthetic")
    for table in ("Objects", "Locations"):
        (game / "Content/Data" / (table + ".xnb")).write_bytes(
            (FIXTURES / (table.lower() + "-synthetic.xnb")).read_bytes()
        )
    (game / "Content/Strings/Objects.pt-BR.xnb").write_bytes(string_table())
    if prior_export:
        out.mkdir()
        for name in ("Objects", "Locations", "ObjectNames"):
            (out / (name + ".json")).write_bytes(
                (FIXTURES / ("artifact-" + name + ".json")).read_bytes()
            )
        (out / "provenance.json").write_text('{"sources": {"previous": "hash"}}')
        assert load_game_data(out).artifact_tables
    original_replace = os.replace
    replacements = 0

    def interrupt(source, destination):
        nonlocal replacements
        replacements += 1
        if replacements == 3:
            raise OSError("simulated disk failure")
        original_replace(source, destination)

    monkeypatch.setattr("stardew.infrastructure.files.os.replace", interrupt)
    with pytest.raises(OSError, match="simulated"):
        export(game, out)
    assert (out / "manifest.json").is_file()
    with pytest.raises(DataError, match="manifest hash mismatch|Missing exported"):
        load_game_data(out, include_maps=False)
    assert not list(out.glob(".*"))


def test_optional_prediction_tables_are_frozen_and_hash_verified(tmp_path):
    import hashlib

    from stardew.api import load_game_data
    from stardew.infrastructure.data_files import DataError

    files = {}
    for name in ("Objects", "Locations", "ObjectNames"):
        files[name + ".json"] = (FIXTURES / ("artifact-" + name + ".json")).read_bytes()
    files["provenance.json"] = b'{"sources":{"Stardew Valley.dll":"synthetic"}}'
    files["MakeoverOutfits.json"] = (
        b'[{"Id":"synthetic", "Gender":null, "OutfitParts":[]}]'
    )
    for name, payload in files.items():
        (tmp_path / name).write_bytes(payload)
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "format_version": 1,
                "game_version": "1.6.15",
                "locale": "en",
                "files": {
                    name: hashlib.sha256(value).hexdigest()
                    for name, value in files.items()
                },
            }
        )
    )
    data = load_game_data(tmp_path, include_maps=False)
    assert data.catalogs["game_MakeoverOutfits"][0]["Id"] == "synthetic"
    with pytest.raises(TypeError):
        data.catalogs["game_MakeoverOutfits"][0]["Id"] = "changed"
    (tmp_path / "MakeoverOutfits.json").write_text('[{"Id":"tampered"}]')
    with pytest.raises(DataError, match="manifest hash mismatch"):
        load_game_data(tmp_path, include_maps=False)
