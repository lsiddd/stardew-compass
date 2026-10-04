"""End-to-end contracts for the unified command and schema."""

import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from stardew.cli import main
from stardew.resources import data_path

FIXTURES = Path(__file__).parents[1] / "fixtures"


@pytest.fixture
def map_save(tmp_path):
    path = tmp_path / "save.xml"
    path.write_text(
        """<SaveGame>
<uniqueIDForThisGame>390938626</uniqueIDForThisGame>
<currentSeason>summer</currentSeason><dayOfMonth>16</dayOfMonth><year>2</year>
<gameVersion>1.6.15</gameVersion><useLegacyRandom>false</useLegacyRandom><whichFarm>1</whichFarm>
<dailyLuck>0.12</dailyLuck>
<player><name>Reference farmer</name><farmName>Reference farm</farmName><stats><Values>
<item><key><string>daysPlayed</string></key><value><unsignedInt>100</unsignedInt></value></item>
<item><key><string>timesFished</string></key><value><unsignedInt>100</unsignedInt></value></item>
</Values></stats><items><Item><itemId>Hoe</itemId></Item></items><mailReceived/></player>
<locations><GameLocation><name>Town</name><objects><item>
<key><Vector2><X>4</X><Y>8</Y></Vector2></key><value><Object><itemId>590</itemId></Object></value>
</item></objects></GameLocation></locations></SaveGame>""",
        encoding="utf-8",
    )
    return path


@pytest.fixture
def artifact_data(tmp_path):
    directory = tmp_path / "tables"
    directory.mkdir()
    for name in ("Objects", "Locations", "ObjectNames"):
        (directory / (name + ".json")).write_bytes(
            (FIXTURES / ("artifact-" + name + ".json")).read_bytes()
        )
    (directory / "provenance.json").write_text(
        json.dumps({"sources": {"synthetic": "a" * 64}})
    )
    return directory


@pytest.mark.parametrize(
    "args", [[], ["predict"], ["--unknown"], ["predict", "bubbles"]]
)
def test_parser_rejects_incomplete_commands(args, capsys):
    with pytest.raises(SystemExit) as error:
        main(args)
    assert error.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_help_and_missing_save(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--help"])
    assert error.value.code == 0
    assert "report" in capsys.readouterr().out
    assert main(["predict", "bubbles", "/nonexistent"]) == 1
    assert capsys.readouterr().err.startswith("Error:")


def test_bubble_json_is_structured_and_working_directory_independent(
    map_save, capsys, monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)
    assert (
        main(
            [
                "predict",
                "bubbles",
                str(map_save),
                "--location",
                "Mountain",
                "--format",
                "json",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["schema_version"] == 2
    assert result["metadata"]["game_version"] == "1.6.15"
    assert result["metadata"]["days_played"] == 100
    assert result["bubbles"]
    assert {event["location"] for event in result["bubbles"]} == {"Mountain"}
    assert all(
        set(event) == {"location", "x", "y", "start", "end", "kind"}
        for event in result["bubbles"]
    )
    assert result["artifacts"] == [] and result["progress"] == []
    assert not captured.err


def test_artifact_data_location_filter_and_single_read(
    map_save, artifact_data, capsys, monkeypatch
):
    original_open, reads = Path.open, []

    def counted_open(self, *args, **kwargs):
        if self == map_save:
            reads.append(self)
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", counted_open)
    args = [
        "predict",
        "artifacts",
        str(map_save),
        "--data-dir",
        str(artifact_data),
        "--format",
        "json",
    ]
    assert main(args) == 0
    result = json.loads(capsys.readouterr().out)
    assert len(result["artifacts"]) == 1
    assert result["artifacts"][0]["location"] == "Town"
    assert reads == [map_save]
    assert main(args + ["--location", "missing"]) == 0
    assert json.loads(capsys.readouterr().out)["artifacts"] == []


def test_isolated_unavailable_features_fail(map_save, capsys):
    assert main(["predict", "artifacts", str(map_save)]) == 1
    assert "exported" in capsys.readouterr().err
    original = map_save.read_text()
    map_save.write_text(original.replace("1.6.15", "1.7.0"))
    assert main(["predict", "bubbles", str(map_save)]) == 1
    assert "1.6.9" in capsys.readouterr().err
    map_save.write_text(
        original.replace("<itemId>Hoe</itemId>", "<itemId>Axe</itemId>")
    )
    assert main(["predict", "artifacts", str(map_save)]) == 1
    assert "exactly one hoe" in capsys.readouterr().err


def test_complete_report_keeps_available_results_and_warns(map_save, capsys):
    assert main(["report", str(map_save), "--format", "json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["schema_version"] == 2
    assert result["bubbles"]
    assert result["progress"]
    assert any(
        diagnostic["feature"] == "artifacts" and diagnostic["severity"] == "warning"
        for diagnostic in result["diagnostics"]
    )


@pytest.mark.parametrize("suffix", [".json", ".resx"])
def test_external_geometry_and_repeated_location_filters(
    map_save, capsys, tmp_path, suffix
):
    maps = json.loads(data_path("maps.json").read_text(encoding="utf-8"))
    selected = {name: maps[name] for name in ("Town", "Mountain")}
    resource = tmp_path / ("maps" + suffix)
    if suffix == ".json":
        resource.write_text(json.dumps(selected))
    else:
        root = ET.Element("root")
        for name, geometry in selected.items():
            node = ET.SubElement(root, "data", name=name)
            ET.SubElement(node, "value").text = json.dumps(geometry)
        resource.write_bytes(ET.tostring(root))
    args = [
        "predict",
        "bubbles",
        str(map_save),
        "--location",
        "Town",
        "--location",
        "Mountain",
        "--format",
        "json",
    ]
    assert main(args) == 0
    expected = json.loads(capsys.readouterr().out)["bubbles"]
    assert main(args + ["--resources", str(resource)]) == 0
    actual = json.loads(capsys.readouterr().out)
    assert actual["bubbles"] == expected
    assert actual["provenance"]["maps"]["source"] == str(resource)


def test_invalid_save_and_output_protection(map_save, capsys, tmp_path):
    original = map_save.read_bytes()
    assert main(["predict", "bubbles", str(map_save), "-o", str(map_save)]) == 1
    assert "overwrite" in capsys.readouterr().err
    assert map_save.read_bytes() == original
    linked = tmp_path / "linked.json"
    linked.symlink_to(map_save)
    assert main(["predict", "bubbles", str(map_save), "-o", str(linked)]) == 1
    capsys.readouterr()
    assert map_save.read_bytes() == original
    map_save.write_text("<broken")
    assert main(["predict", "bubbles", str(map_save)]) == 1
    assert "XML" in capsys.readouterr().err


def test_json_file_and_text_results(map_save, capsys, tmp_path):
    args = ["predict", "bubbles", str(map_save), "--location", "Town"]
    assert main(args + ["--format", "json"]) == 0
    expected = json.loads(capsys.readouterr().out)
    output = tmp_path / "report.json"
    assert main(args + ["--format", "json", "-o", str(output)]) == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(output.read_text()) == expected
    assert main(args) == 0
    assert "Town" in capsys.readouterr().out
    assert not list(tmp_path.glob(".report.json.*"))


def test_cli_plot_validation_and_json_stability(
    map_save, capsys, monkeypatch, tmp_path
):
    assert main(["predict", "bubbles", str(map_save), "--plot", str(tmp_path)]) == 1
    assert "--game-dir" in capsys.readouterr().err
    calls = []

    def fake_plot(state, results, output, game, mode):
        calls.append((state.metadata.days_played, len(results), mode))
        return [Path(output) / "Town.png"]

    monkeypatch.setattr("stardew.presentation.maps.save_plots", fake_plot)
    args = [
        "predict",
        "bubbles",
        str(map_save),
        "--location",
        "Town",
        "--format",
        "json",
    ]
    assert main(args) == 0
    expected = json.loads(capsys.readouterr().out)
    assert main(args + ["--plot", str(tmp_path), "--game-dir", "game"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out) == expected
    assert "Saved figure:" in captured.err
    assert calls and calls[0][0] == 100 and calls[0][-1] == "bubbles"


def test_decimal_bounds_and_version_normalization(map_save, capsys):
    original = map_save.read_text()
    map_save.write_text(original.replace("1.6.15", "01.06.015"))
    assert main(["predict", "bubbles", str(map_save), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["metadata"]["game_version"] == "1.6.15"
    for invalid in ("9223372036854775808", "390_938_626"):
        map_save.write_text(original.replace("390938626", invalid))
        assert main(["predict", "bubbles", str(map_save)]) == 1
        assert capsys.readouterr().err.startswith("Error:")


def test_unknown_location_and_export_errors(map_save, capsys, tmp_path):
    assert main(["predict", "bubbles", str(map_save), "--location", "missing"]) == 1
    assert "Unsupported" in capsys.readouterr().err
    assert (
        main(["data", "export", "/nonexistent", "--output", str(tmp_path / "out")]) == 1
    )
    assert capsys.readouterr().err.startswith("Error:")


def test_selected_report_section_has_no_unrequested_map_calculations(map_save, capsys):
    assert (
        main(["report", str(map_save), "--section", "skills", "--format", "json"]) == 0
    )
    result = json.loads(capsys.readouterr().out)
    assert [section["section_id"] for section in result["progress"]] == ["skills"]
    assert (
        result["predictions"] == []
        and result["bubbles"] == []
        and result["artifacts"] == []
    )


def test_calendar_interval_spans_native_month_pages(map_save, capsys):
    assert (
        main(
            [
                "predict",
                "mines",
                str(map_save),
                "--start",
                "1",
                "--count",
                "56",
                "--format",
                "json",
            ]
        )
        == 0
    )
    result = json.loads(capsys.readouterr().out)
    records = result["predictions"][0]["records"]
    assert [record["date"]["days_played"] for record in records] == list(range(1, 57))
