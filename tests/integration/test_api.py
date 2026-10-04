import json
from pathlib import Path
from dataclasses import replace
import pytest
from stardew.api import load_save, load_game_data, analyze, AnalysisOptions
from stardew.presentation.json import render_json
from stardew.presentation.text import render_text
from stardew.domain.errors import FeatureUnavailable


@pytest.fixture
def simple_state(tmp_path):
    path = tmp_path / "Farmer_42"
    path.write_text("""<SaveGame><uniqueIDForThisGame>42</uniqueIDForThisGame>
      <player><name>Ana</name></player></SaveGame>""")
    return load_save(path)


def test_renderers_repeat_without_mutation(simple_state):
    data = load_game_data()
    options = AnalysisOptions(
        progress=(), predictions=(), bubbles=False, artifacts=False
    )
    first = analyze(simple_state, data=data, options=options)
    before = render_json(first)
    assert "Inventory: Ana" in render_text(first, data=data)
    assert render_json(first) == before
    assert analyze(simple_state, data=data, options=options) == first
    with pytest.raises(TypeError):
        data.catalogs["checkup_shipping"]["bogus"] = "mutation"
    with pytest.raises(TypeError):
        data.maps["Town"].layers["Back"]["width"] = 0


def test_expected_unavailable_features_warn_or_raise(simple_state):
    data = load_game_data()
    report = analyze(
        simple_state, data=data, options=AnalysisOptions(progress=(), predictions=())
    )
    assert {diagnostic.feature for diagnostic in report.diagnostics} == {
        "bubbles",
        "artifacts",
    }
    with pytest.raises(FeatureUnavailable):
        analyze(
            simple_state,
            data=data,
            options=AnalysisOptions(progress=(), predictions=(), strict=True),
        )


def test_internal_errors_remain_explicit(simple_state, monkeypatch):
    from stardew.domain.predictions import bubbles

    def fail(*args, **kwargs):
        raise RuntimeError("broken calculation")

    monkeypatch.setattr(bubbles, "predict_bubbles", fail)
    with pytest.raises(RuntimeError, match="broken calculation"):
        analyze(
            simple_state,
            data=load_game_data(),
            options=AnalysisOptions(progress=(), predictions=(), artifacts=False),
        )


def test_external_data_requires_provenance(tmp_path):
    for name in ("Objects", "Locations", "ObjectNames"):
        (tmp_path / (name + ".json")).write_text('{"one": "two"}')
    with pytest.raises(ValueError, match="provenance"):
        load_game_data(tmp_path)
    (tmp_path / "provenance.json").write_text('{"sources": {"synthetic": "hash"}}')
    data = load_game_data(tmp_path)
    assert data.provenance["game_tables"]["sources"]["synthetic"] == "hash"
    with pytest.raises(TypeError):
        data.artifact_tables["Objects"]["one"] = "changed"


def test_analysis_options_freeze_inputs_and_accept_nested_prediction_settings(
    simple_state,
):
    from types import MappingProxyType
    from stardew.api import ReportPredictionOptions

    sections = ["summary"]
    options = AnalysisOptions(
        progress=sections,
        predictions=(),
        bubbles=False,
        artifacts=False,
        prediction_options={"start": 1, "count": 1},
    )
    sections.append("money")
    assert options.progress == ("summary",)
    assert options.prediction_options == ReportPredictionOptions(start=1, count=1)
    result = analyze(
        simple_state,
        data=load_game_data(),
        options=MappingProxyType(
            {
                "progress": ["summary"],
                "predictions": (),
                "bubbles": False,
                "artifacts": False,
            }
        ),
    )
    assert tuple(section.section_id for section in result.progress) == ("summary",)
    with pytest.raises(TypeError, match="progress"):
        AnalysisOptions(progress="summary")
    with pytest.raises(TypeError, match="prediction_options"):
        AnalysisOptions(prediction_options=object())
