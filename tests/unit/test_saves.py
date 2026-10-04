import io
import contextlib
import json
import os
from pathlib import Path
from unittest.mock import patch
import zlib

import pytest
from stardew.api import load_save
from stardew.infrastructure.saves import SaveError, atomic_write, check_output_path
from stardew.infrastructure.saves import loader
from stardew.cli import main

MINIMAL = b"<SaveGame><player><name>Ana</name></player><uniqueIDForThisGame>42</uniqueIDForThisGame></SaveGame>"


def test_typed_saved_fields_preserve_absence_zero_and_false(tmp_path):
    path = tmp_path / "save"
    path.write_bytes(MINIMAL)
    missing = load_save(path)
    assert missing.player.total_money_earned is None
    assert missing.player.has_special_charm is None
    assert missing.world.perfection_waivers is None
    assert missing.metadata.game_version is None
    assert missing.rules_version == "1.2"
    fields = b"""<totalMoneyEarned>0</totalMoneyEarned><hasSpecialCharm>false</hasSpecialCharm>
      <gender>Female</gender><eventsSeen><int>191393</int></eventsSeen>"""
    world = b"""<perfectionWaivers>0</perfectionWaivers>
      <hasApplied1_4_UpdateChanges>true</hasApplied1_4_UpdateChanges>"""
    path.write_bytes(
        MINIMAL.replace(b"</player>", fields + b"</player>").replace(
            b"</SaveGame>", world + b"</SaveGame>"
        )
    )
    present = load_save(path)
    assert present.player.total_money_earned == 0
    assert present.player.has_special_charm is False
    assert present.player.gender == "Female"
    assert present.player.events == frozenset({"191393"})
    assert present.world.perfection_waivers == 0
    assert present.metadata.game_version is None
    assert present.rules_version == "1.4"


@pytest.mark.parametrize(
    "encoded",
    [
        MINIMAL,
        b"\xef\xbb\xbf\n  " + MINIMAL,
        zlib.compress(MINIMAL),
        ('<?xml version="1.0" encoding="utf-16"?>' + MINIMAL.decode()).encode("utf-16"),
    ],
)
def test_encoded_saves_read_once(tmp_path, encoded):
    path = tmp_path / "Ana_42"
    path.write_bytes(encoded)
    real_open = Path.open
    opened = []

    def tracked_open(source, *args, **kwargs):
        opened.append(source)
        return real_open(source, *args, **kwargs)

    with patch.object(Path, "open", tracked_open):
        state = load_save(path)
    assert opened == [path]
    assert state.player.name == "Ana"
    assert state.metadata.days_played is None
    assert state.metadata.use_legacy_random is None
    with pytest.raises(TypeError):
        state.player.stats["daysPlayed"] = 0
    with pytest.raises(AttributeError):
        state.metadata.day = 1
    assert path.read_bytes() == encoded


def test_save_folder(tmp_path):
    folder = tmp_path / "Ana_42"
    folder.mkdir()
    (folder / folder.name).write_bytes(MINIMAL)
    assert load_save(folder).source.name == "Ana_42"


@pytest.mark.parametrize(
    "content",
    [
        b"",
        b"not XML",
        b"<SaveGame>",
        b"<Farmer><name>Ana</name></Farmer>",
        b"<SaveGame/>",
        zlib.compress(MINIMAL)[:-2],
        zlib.compress(MINIMAL) + b"junk",
        b'<!DOCTYPE SaveGame [<!ENTITY x SYSTEM "file:///etc/passwd">]>' + MINIMAL,
    ],
)
def test_invalid_saves(tmp_path, content):
    path = tmp_path / "Ana_42"
    path.write_bytes(content)
    with pytest.raises(SaveError):
        load_save(path)


def test_decompressed_limit(tmp_path, monkeypatch):
    path = tmp_path / "save"
    path.write_bytes(zlib.compress(b" " * 10000))
    monkeypatch.setattr(loader, "MAX_SAVE_BYTES", 100)
    with pytest.raises(SaveError, match="limit"):
        load_save(path)


def test_output_protects_input_and_links(tmp_path):
    path, hard, sym = (tmp_path / name for name in ("save", "hard", "sym"))
    path.write_bytes(MINIMAL)
    os.link(path, hard)
    sym.symlink_to(path)
    for output in (path, hard, sym):
        with pytest.raises(SaveError):
            check_output_path(output, path)


def test_atomic_failure_keeps_previous_output(tmp_path):
    path = tmp_path / "report"
    path.write_text("previous")
    with patch(
        "stardew.infrastructure.files.os.replace", side_effect=OSError("disk failure")
    ):
        with pytest.raises(OSError):
            atomic_write(path, "replacement")
    assert path.read_text() == "previous"
    assert list(tmp_path.iterdir()) == [path]


def test_cli_structured_extras_and_input_protection(tmp_path, capsys):
    path = tmp_path / "save"
    path.write_bytes(MINIMAL)
    assert main(["report", str(path), "--only", "extras", "--format", "json"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["schema_version"] == 2
    assert output["extras"]["players"][0]["name"] == "Ana"
    assert "snapshot" not in json.dumps(output)
    assert main(["report", str(path), "-o", str(path), "--only", "extras"]) == 1
    assert path.read_bytes() == MINIMAL


def test_days_played_is_not_calendar_date(tmp_path):
    path = tmp_path / "save"
    path.write_text("""<SaveGame><uniqueIDForThisGame>9007199254740993</uniqueIDForThisGame>
      <year>9</year><currentSeason>winter</currentSeason><dayOfMonth>28</dayOfMonth>
      <useLegacyRandom>false</useLegacyRandom><player><name>Ana</name><stats><Values>
      <item><key>\n<string>daysPlayed</string></key><value>\n<unsignedInt>0</unsignedInt></value></item>
      </Values></stats></player></SaveGame>""")
    state = load_save(path)
    assert state.metadata.days_played == 0
    assert state.metadata.game_id == 9007199254740993
    assert state.metadata.use_legacy_random is False
    assert state.metadata.farm_type is None


def test_duplicate_animal_serializations_and_invalid_statistic(tmp_path):
    animal = "<item><value><FarmAnimal><myID>9007199254740993</myID><name>Bella</name><age>12</age></FarmAnimal></value></item>"
    path = tmp_path / "save"
    body = f"<locations><GameLocation><animals>{animal}</animals><Animals>{animal}</Animals></GameLocation></locations>"
    path.write_bytes(MINIMAL.replace(b"</SaveGame>", body.encode() + b"</SaveGame>"))
    state = load_save(path)
    assert len(state.world.animals) == 1
    assert state.world.animals[0].animal_id == 9007199254740993
    stats = "<stats><Values><item><key><string>daysPlayed</string></key><value><unsignedInt>1_000</unsignedInt></value></item></Values></stats>"
    path.write_bytes(MINIMAL.replace(b"</player>", stats.encode() + b"</player>"))
    with pytest.raises(SaveError, match="statistic"):
        load_save(path)
