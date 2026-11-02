"""Public regressions for the architecture and correctness review."""

import json
from dataclasses import dataclass, replace

import pytest
from jsonschema import Draft202012Validator

from stardew.api import (
    AnalysisOptions,
    ReportPredictionOptions,
    analyze,
    load_game_data,
    load_save,
)
from stardew.domain.errors import FeatureUnavailable
from stardew.domain.models.state import SaveNode, freeze
from stardew.domain.numeric import MAX, SystemRandom, i32
from stardew.domain.predictions.registry import FEATURES, REGISTRY
from stardew.domain.predictions.report_predictions import analyze_predictions
from stardew.domain.predictions.report_support import compare_version
from stardew.domain.progress.common import number
from stardew.domain.values import GameVersion
from stardew.infrastructure.data_files import DataError, read_json
from stardew.infrastructure.game_data.maps import read_maps
from stardew.presentation.json import render_json, to_data
from stardew.resources import data_path


@pytest.fixture
def state(tmp_path):
    path = tmp_path / "Farmer_390938626"
    path.write_text(
        """<SaveGame><uniqueIDForThisGame>390938626</uniqueIDForThisGame>
<gameVersion>1.6.15</gameVersion><year>2</year><currentSeason>spring</currentSeason>
<dayOfMonth>10</dayOfMonth><dailyLuck>0.02</dailyLuck><useLegacyRandom>false</useLegacyRandom><whichFarm>0</whichFarm>
<player><name>Host</name><UniqueMultiplayerID>101</UniqueMultiplayerID><deepestMineLevel>120</deepestMineLevel>
<stats><daysPlayed>122</daysPlayed><geodesCracked>20</geodesCracked><trashCansChecked>100</trashCansChecked></stats>
<items><Item><itemId>Hoe</itemId></Item></items></player></SaveGame>""",
        encoding="utf-8",
    )
    return load_save(path)


@pytest.fixture
def data():
    return load_game_data(include_maps=False)


@pytest.mark.parametrize(
    "field,value",
    [("extras", "false"), ("bubbles", 0), ("artifacts", None), ("strict", 1)],
)
def test_analysis_rejects_non_boolean_switches(field, value):
    with pytest.raises(TypeError, match=field):
        AnalysisOptions(**{field: value})


@pytest.mark.parametrize(
    "field,value",
    [
        ("day_offset", None),
        ("luck_level", True),
        ("game_start", 1.2),
        ("item_filter", 123),
        ("daily_luck", "0.1"),
        ("player_indices", (0, True)),
    ],
)
def test_prediction_options_fail_at_the_boundary(field, value):
    with pytest.raises(TypeError, match=field):
        ReportPredictionOptions(**{field: value})


@pytest.mark.parametrize(
    "luck", [float("nan"), float("inf"), float("-inf"), -0.11, 0.11]
)
def test_prediction_luck_is_finite_and_bounded(luck):
    with pytest.raises(ValueError, match="daily_luck"):
        ReportPredictionOptions(daily_luck=luck)


def test_version_and_large_integer_contracts():
    assert compare_version("1.6", "1.6.0") == 0
    assert GameVersion.parse("01.06.015") == GameVersion.parse("1.6.15.0")
    assert GameVersion.parse("1.6.15.1") > GameVersion.parse("1.6.15")
    assert number("9007199254740993") == 9007199254740993
    assert number("-9223372036854775808") == -9223372036854775808


def test_world_predictions_are_not_repeated_for_each_player(state, data):
    guest = replace(
        state.player,
        name="Guest",
        player_id=202,
        deepest_mine_level=0,
        has_special_charm=True,
        mail=frozenset({"GotMysteryBook"}),
    )
    state = replace(state, players=(state.player, guest))
    options = ReportPredictionOptions(start=64, count=1, player_indices=(0, 1, 1))
    train, geodes = analyze_predictions(state, data, ("train", "geode"), options)
    assert len(train.records) == 1
    assert train.records[0].player_id is None
    assert len(geodes.records) == 12
    assert {r.player_id for r in geodes.records} == {101, 202}
    assert options.player_indices == (0, 1)


@pytest.mark.parametrize("feature", ["geode", "mystery", "cj", "statue"])
def test_selected_guest_uses_own_flags_luck_and_mine_depth(state, data, feature):
    guest = replace(
        state.player,
        name="Guest",
        player_id=202,
        deepest_mine_level=0,
        has_special_charm=True,
        mail=frozenset({"GotMysteryBook"}),
        stats=freeze({"Book_Trash": 1, "trashCansChecked": 0}),
    )
    state = replace(
        state,
        players=(
            replace(
                state.player,
                mail=frozenset(
                    {"ccVault", "ccMovieTheater", "ccCraftsRoom", "ccPantry"}
                ),
                events=frozenset({"191393"}),
            ),
        ),
    )
    multiplayer = replace(state, players=(state.player, guest))
    options = ReportPredictionOptions(start=57, count=28, player_indices=(1,))
    selected = analyze_predictions(multiplayer, data, (feature,), options)[0]
    alone = analyze_predictions(
        replace(state, players=(guest,)),
        data,
        (feature,),
        replace(options, player_indices=(0,)),
    )[0]
    # Internal player array positions differ; every public predicted outcome agrees.
    assert [replace(r, facts=()) for r in selected.records] == [
        replace(r, facts=()) for r in alone.records
    ]

    def relevant_facts(records):
        return [
            tuple(f for f in r.facts if f.name not in ("which_player", "player"))
            for r in records
        ]

    assert relevant_facts(selected.records) == relevant_facts(alone.records)


def test_missing_player_ids_are_not_invented(state, data):
    state = replace(state, players=(replace(state.player, player_id=None),))
    with pytest.raises(FeatureUnavailable, match="player ID"):
        analyze_predictions(state, data, ("geode",), ReportPredictionOptions(count=1))
    legacy = replace(state, metadata=replace(state.metadata, game_version="1.5"))
    records = analyze_predictions(
        legacy, data, ("geode",), ReportPredictionOptions(count=1)
    )[0].records
    assert records and all(r.player_id is None for r in records)
    assert state.player.identity(0) == "player_0"


def test_sequence_does_not_require_a_saved_day(state, data):
    state = replace(state, metadata=replace(state.metadata, days_played=None))
    records = analyze_predictions(
        state, data, ("geode",), ReportPredictionOptions(count=2)
    )[0].records
    assert {r.sequence for r in records} == {21, 22}


@pytest.mark.parametrize("feature", [f.identifier for f in FEATURES if f.counter])
@pytest.mark.parametrize("counter", [0, 1, 19, 20, 21, 467])
def test_default_sequence_starts_after_saved_counter(state, data, feature, counter):
    spec = REGISTRY[feature]
    if feature == "raccoon":
        state = replace(state, world=replace(state.world, times_fed_raccoons=counter))
    else:
        stat = "MysteryBoxesOpened" if feature == "mystery" else spec.counter
        state = replace(
            state,
            players=(
                replace(
                    state.player, stats=freeze({**state.player.stats, stat: counter})
                ),
            ),
        )
    default = analyze_predictions(state, data, (feature,))[0].records
    explicit = analyze_predictions(
        state,
        data,
        (feature,),
        ReportPredictionOptions(start=counter + 1, count=spec.page_size),
    )[0].records
    assert default == explicit
    assert {r.sequence for r in default} == set(
        range(counter + 1, counter + spec.page_size + 1)
    )


@pytest.mark.parametrize(
    "feature", [f.identifier for f in FEATURES if f.range_kind == "days"]
)
def test_default_calendar_starts_today_and_matches_explicit_count(state, data, feature):
    default = analyze_predictions(state, data, (feature,))[0].records
    explicit = analyze_predictions(
        state,
        data,
        (feature,),
        ReportPredictionOptions(count=REGISTRY[feature].page_size),
    )[0].records
    assert default == explicit
    assert all(r.date.days_played >= state.metadata.days_played for r in default)


def test_geode_next_number_and_relative_position_follow_selected_player(state, data):
    host = replace(
        state.player, stats=freeze({**state.player.stats, "geodesCracked": 467})
    )
    guest = replace(
        host, name="Guest", player_id=202, stats=freeze({"geodesCracked": 8})
    )
    state = replace(state, players=(host, guest))
    section = analyze_predictions(state, data, ("geode",))[0]
    for player_id, saved in ((host.player_id, 467), (guest.player_id, 8)):
        rows = [r for r in section.records if r.player_id == player_id]
        assert min(r.sequence for r in rows) == saved + 1
        assert max(r.sequence for r in rows) == saved + 20
        for row in rows:
            facts = {f.name: f.value for f in row.facts}
            assert facts["saved_counter"] == saved
            assert facts["openings_ahead"] == row.sequence - saved


def test_explicit_sequence_can_inspect_past_openings(state, data):
    records = analyze_predictions(
        state, data, ("geode",), ReportPredictionOptions(start=1, count=2)
    )[0].records
    assert {r.sequence for r in records} == {1, 2}
    assert all(
        dict((f.name, f.value) for f in r.facts)["openings_ahead"] < 0 for r in records
    )


@pytest.mark.parametrize("joja_member", [False, True])
def test_cart_catalogues_use_completed_host_areas_before_ceremony(
    state, data, joja_member
):
    # Shops/Traveler queries completion mail, independently of ceremony events.
    mail = frozenset(
        "cc" + area
        for area in (
            "BoilerRoom",
            "CraftsRoom",
            "Pantry",
            "FishTank",
            "Vault",
            "Bulletin",
        )
    )
    if joja_member:
        mail |= {"JojaMember"}
    state = replace(
        state, players=(replace(state.player, mail=mail, events=frozenset()),)
    )
    rows = analyze_predictions(
        state, data, ("cart",), ReportPredictionOptions(start=1, count=112)
    )[0].records
    catalogues = {
        r.item_name for r in rows if r.item_name and "Catalogue" in r.item_name
    }
    assert "Junimo Catalogue" in catalogues
    assert ("Joja Catalogue" in catalogues) is not joja_member


def test_cart_ceremony_does_not_replace_completion_mail_checks(state, data):
    state = replace(
        state,
        players=(
            replace(
                state.player, mail=frozenset(), events=frozenset({"191393", "502261"})
            ),
        ),
    )
    rows = analyze_predictions(
        state, data, ("cart",), ReportPredictionOptions(start=1, count=112)
    )[0].records
    assert not any(r.item_name in ("Joja Catalogue", "Junimo Catalogue") for r in rows)


def test_desert_festival_cart_requires_host_bus_unlock(state, data):
    options = ReportPredictionOptions(start=15, count=3)
    assert not analyze_predictions(state, data, ("cart",), options)[0].records
    state = replace(
        state, players=(replace(state.player, mail=frozenset({"ccVault"})),)
    )
    rows = analyze_predictions(state, data, ("cart",), options)[0].records
    assert {r.date.days_played for r in rows} == {15, 16, 17}


def test_wallpaper_access_uses_any_players_ceremony(state, data):
    guest = replace(state.player, player_id=202, events=frozenset({"191393"}))
    state = replace(state, players=(state.player, guest))
    rows = analyze_predictions(
        state, data, ("wallpaper",), ReportPredictionOptions(start=3, count=1)
    )[0].records
    pierre = [r for r in rows if r.location == "Pierre"]
    joja = [r for r in rows if r.location == "JojaMart"]
    assert {r.item_name for r in pierre} == {"Wallpaper", "Flooring"}
    assert (
        len(joja) == 1
        and dict((f.name, f.value) for f in joja[0].facts)["open"] is False
    )


@pytest.mark.parametrize(
    "day,closed",
    [
        (13, True),
        (24, True),
        (39, True),
        (56, False),
        (72, True),
        (83, False),
        (92, True),
        (109, True),
    ],
)
def test_wallpaper_closes_only_for_daytime_festivals(state, data, day, closed):
    rows = analyze_predictions(
        state, data, ("wallpaper",), ReportPredictionOptions(start=day, count=1)
    )[0].records
    if closed:
        assert len(rows) == 2
        assert all(
            dict((f.name, f.value) for f in r.facts)["open"] is False for r in rows
        )
    else:
        assert {r.item_name for r in rows} == {"Wallpaper", "Flooring"}


def test_wallpaper_wednesday_key_access_is_conditional(state, data):
    state = replace(
        state, players=(replace(state.player, mail=frozenset({"HasTownKey"})),)
    )
    rows = analyze_predictions(
        state, data, ("wallpaper",), ReportPredictionOptions(start=3, count=1)
    )[0].records
    pierre = [r for r in rows if r.location == "Pierre"]
    assert len(pierre) == 2
    assert all(
        "Pierre must be serving"
        in dict((f.name, f.value) for f in r.facts)["access_condition"]
        for r in pierre
    )


def test_calendar_window_is_composable_across_season_and_year(state, data):
    sections = ("train", "night", "trash", "greenrain", "statue")
    first = analyze_predictions(
        state, data, sections, ReportPredictionOptions(start=110, count=3)
    )
    second = analyze_predictions(
        state, data, sections, ReportPredictionOptions(start=113, count=3)
    )
    combined = analyze_predictions(
        state, data, sections, ReportPredictionOptions(start=110, count=6)
    )
    assert [a.records + b.records for a, b in zip(first, second, strict=True)] == [
        s.records for s in combined
    ]


def test_trash_does_not_inherit_previous_can_quantity(state, data):
    state = replace(
        state,
        players=(
            replace(
                state.player,
                stats=freeze({**state.player.stats, "trashCansChecked": 44}),
            ),
        ),
    )
    records = analyze_predictions(
        state,
        data,
        ("trash",),
        ReportPredictionOptions(start=64, count=1, daily_luck=0.1),
    )[0].records
    cookie = next(
        record
        for record in records
        if record.location == "Alex" and record.item_name == "Cookie"
    )
    assert cookie.quantity == 1


def test_non_arriving_train_has_no_stale_time(state, data):
    records = analyze_predictions(
        state, data, ("train",), ReportPredictionOptions(start=31, count=112)
    )[0].records
    assert any(record.time is not None for record in records)
    assert any(record.time is None for record in records)
    for record in records:
        facts = {f.name: f.value for f in record.facts}
        assert facts["arrives"] == (record.time is not None)
        assert facts["train_time"] == record.time


def test_public_execution_does_not_copy_capture_locals(state, data, monkeypatch):
    from stardew.domain.predictions import report_support

    def fail(_value):
        raise AssertionError("production retained legacy captures")

    monkeypatch.setattr(report_support, "deepcopy", fail)
    assert analyze_predictions(
        state, data, ("train",), ReportPredictionOptions(count=1)
    )[0].records


def test_json_has_explicit_contract_and_assumptions(state, data):
    result = analyze(
        state,
        data=data,
        options=AnalysisOptions(
            progress=("summary", "skills"),
            predictions=("train", "geode"),
            bubbles=False,
            artifacts=False,
            prediction_options={"start": 31, "count": 1},
        ),
    )
    payload = json.loads(render_json(result))
    schema = json.loads(data_path("report-v2.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(payload)
    assert (
        payload["provenance"]["analysis"]["prediction_settings"]["base_daily_luck"]
        == -0.1
    )
    assert payload["provenance"]["analysis"]["requested"]["bubbles"] is False
    assert "snapshot" not in render_json(result)
    assert "contributions" not in render_json(result)

    @dataclass
    class InternalDetail:
        secret: str

    with pytest.raises(TypeError, match="public JSON contract"):
        to_data(InternalDetail("internal"))


@pytest.mark.parametrize("literal", ["NaN", "Infinity", "-Infinity", "1e999"])
def test_json_rejects_nonfinite_numbers_with_source(tmp_path, literal):
    path = tmp_path / "invalid.json"
    path.write_text('{"value": ' + literal + "}")
    with pytest.raises(DataError, match="invalid.json.*non-finite"):
        read_json(path)


@pytest.mark.parametrize(
    "geometry",
    [
        {},
        {"width": True, "height": 20, "layers": [], "tilesets": []},
        {"width": 1, "height": 1, "layers": [{"name": "Back"}], "tilesets": []},
    ],
)
def test_geometry_errors_identify_source_and_location(tmp_path, geometry):
    path = tmp_path / "maps.json"
    path.write_text(json.dumps({"Town": geometry}))
    with pytest.raises(DataError, match="maps.json.*Town"):
        read_maps(path)


def test_snapshot_paths_are_lazy_ordered_and_do_not_retain_saves():
    from stardew.domain.models.saved_paths import compile_path

    first = SaveNode(
        "item", attributes=freeze({"id": "a/b"}), children=(SaveNode("name", "first"),)
    )
    second = SaveNode("item", children=(SaveNode("name", "second"),))
    root = SaveNode("root", children=(first, SaveNode("nested", children=(second,))))
    assert root.findall(".//item/name") == (first.children[0], second.children[0])
    assert root.find("item[@id='a/b']/name").text() == "first"
    assert root.find(".//item[name='second']") is second
    assert next(root.iterfind(".//item")) is first
    assert compile_path.cache_info().maxsize == 512


def test_optimized_random_matches_reference_arithmetic_for_extreme_seeds():
    # Independent implementation of the pre-optimization constructor.
    def reference(seed):
        seed = i32(seed)
        mj = 161803398 - (MAX if seed == -2147483648 else abs(seed))
        values = [0] * 56
        values[55], mk = mj, 1
        for i in range(1, 55):
            index = 21 * i % 55
            values[index] = mk
            mk = i32(mj - mk)
            if mk < 0:
                mk += MAX
            mj = values[index]
        for _ in range(4):
            for i in range(1, 56):
                values[i] = i32(values[i] - values[1 + (i + 30) % 55])
                if values[i] < 0:
                    values[i] += MAX
        return values

    seeds = [-(2**63), -2147483648, -2147483647, -1, 0, 1, MAX, 2**63 - 1]
    seeds.extend(i32(index * 2654435761) for index in range(1000))
    for seed in seeds:
        assert SystemRandom(seed).values == reference(seed)


def test_bounded_reads_allocate_for_contents_not_input_limit():
    from io import BytesIO

    from stardew.infrastructure.streams import read_bounded

    class RecordingStream(BytesIO):
        def read(self, size=-1):
            assert 0 <= size <= 1024 * 1024
            return super().read(size)

    assert read_bounded(RecordingStream(b"small"), 128 * 1024 * 1024) == b"small"
    assert read_bounded(RecordingStream(b"123456789"), 4) == b"12345"


@pytest.mark.parametrize(
    "condition", [False, 0, 1, "RANDOM NaN", "DAYS_PLAYED", "RANDOM 1.01"]
)
def test_artifact_conditions_reject_invalid_contracts(condition):
    from stardew.domain.predictions.artifact_conditions import compile_condition

    with pytest.raises(ValueError):
        compile_condition(condition)


def test_text_preserves_recipe_status_and_equipment_enchantments(state, data):
    from stardew.domain.progress.models import ProgressItem
    from stardew.presentation.text import progress_item_line, render_text

    line = progress_item_line(
        ProgressItem("recipe", "Recipe", category="unknown_recipe")
    )
    assert "unknown_recipe" in line
    hoe = replace(
        state.player.inventory[0], enchantments=frozenset({"GenerousEnchantment"})
    )
    state = replace(state, players=(replace(state.player, inventory=(hoe,)),))
    result = analyze(
        state,
        data=data,
        options=AnalysisOptions(
            progress=(), predictions=(), bubbles=False, artifacts=False
        ),
    )
    assert "GenerousEnchantment" in render_text(result, data=data)


def test_exported_binary_hash_selects_verified_train_profile(state, data):
    state = replace(state, metadata=replace(state.metadata, game_id=390938626))
    verified = replace(
        data,
        provenance=freeze(
            {
                "game_tables": {
                    "sources": {
                        "Stardew Valley.dll": "F3E97F01D3FD2B1E6094FC8D2B59950AA6CB9D6CD1BF1B39D72D58EDDA8AAD12",
                    }
                }
            }
        ),
    )
    options = ReportPredictionOptions(start=124, count=1)
    row = analyze_predictions(state, verified, ("train",), options)[0].records[0]
    assert row.time == 900
    assert {fact.name: fact.value for fact in row.facts}[
        "verification"
    ] == "matched_installed_dll"
    fallback = analyze_predictions(state, data, ("train",), options)[0].records[0]
    assert fallback.time == 1320
    assert {fact.name: fact.value for fact in fallback.facts}[
        "verification"
    ] == "unverified_historical_rule"
