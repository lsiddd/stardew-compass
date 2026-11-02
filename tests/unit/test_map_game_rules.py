"""Corrections anchored in separately captured DLL/xTile observations.

The fixture came from .NET 6 and the installed 1.6.15 assembly, not Python.
See docs/maps-game-parity.md for the method and remaining runtime boundaries.
"""

import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from stardew.api import AnalysisOptions, analyze, load_game_data, load_save
from stardew.domain.errors import FeatureUnavailable
from stardew.domain.models.maps import Map
from stardew.domain.numeric import Random
from stardew.domain.predictions import bubbles
from stardew.domain.predictions.artifact_conditions import compile_condition
from stardew.domain.predictions.artifacts import (
    ArtifactPredictor,
    ArtifactSpot,
    ArtifactState,
    condition,
    location_context,
    location_season,
)
from stardew.presentation.json import render_json
from stardew.presentation.maps import rows_for_results
from stardew.presentation.text import render_text

FIXTURES = Path(__file__).parents[1] / "fixtures"
ORACLE = json.loads((FIXTURES / "game-map-rules.json").read_text())
CONTEXT_ORACLE = json.loads((FIXTURES / "game-artifact-contexts.json").read_text())


def metadata(day, seed=390938626, fish_count=3):
    year, remaining = divmod(day - 1, 112)
    season, date = divmod(remaining, 28)
    return SimpleNamespace(
        game_id=seed,
        days_played=day,
        year=year + 1,
        season=("spring", "summer", "fall", "winter")[season],
        day=date + 1,
        game_version="1.6.15",
        use_legacy_random=False,
        farm_type=0,
        fish_caught_count=fish_count,
        daily_luck=-0.008,
    )


@pytest.fixture(scope="module")
def maps():
    return load_game_data().maps


@pytest.fixture(scope="module")
def artifacts():
    return ArtifactPredictor(
        {
            name: json.loads((FIXTURES / f"artifact-{name}.json").read_text())
            for name in ("Locations", "Objects", "ObjectNames")
        }
    )


@pytest.fixture
def state(tmp_path):
    path = tmp_path / "Farmer_390938626"
    path.write_text(
        """<SaveGame><uniqueIDForThisGame>390938626</uniqueIDForThisGame>
<gameVersion>1.6.15</gameVersion><year>2</year><currentSeason>spring</currentSeason>
<dayOfMonth>15</dayOfMonth><dailyLuck>-0.008</dailyLuck><useLegacyRandom>false</useLegacyRandom><whichFarm>0</whichFarm>
<player><name>Host</name><UniqueMultiplayerID>101</UniqueMultiplayerID>
<stats><daysPlayed>127</daysPlayed><ArtifactSpotsDug>171</ArtifactSpotsDug></stats>
<mailReceived><string>HasSpecialCharm</string><string>HasMagnifyingGlass</string></mailReceived>
<mailForTomorrow><string>guntherBones%&amp;NL&amp;%</string></mailForTomorrow>
<items><Item><itemId>Hoe</itemId></Item></items></player></SaveGame>""",
        encoding="utf-8",
    )
    return load_save(path)


@pytest.mark.parametrize("observation", ORACLE["geometry"])
def test_distance_and_instance_properties_match_game_dll(observation, maps):
    map = maps[observation["location"]]
    x, y = observation["x"], observation["y"]
    assert map.distance_to_land(x, y) == observation["depth"]
    assert map.property(x, y, "NoFishing") is observation["no_fishing"]


def test_global_gid_is_resolved_before_outdoors_blocking(maps):
    # Original xTile: Mountain(54,20)=outdoors:629/GID630;
    # Mountain(46,6)=outdoors:758/GID759.
    assert maps["Mountain"].tile_index(54, 20, "Buildings", "outdoors") == 629
    assert not maps["Mountain"].open_water(54, 20)
    assert maps["Mountain"].tile_index(46, 6, "Buildings", "outdoors") == 758
    assert maps["Mountain"].open_water(46, 6)


def test_first_gid_and_tilesheet_identity_are_not_discarded():
    map = Map(
        {
            "width": 1,
            "height": 1,
            "layers": [
                {"name": "Back", "width": 1, "data": [1]},
                {"name": "Buildings", "width": 1, "data": [629]},
            ],
            "tilesets": [
                {
                    "firstgid": 1,
                    "name": "other-sheet",
                    "tiles": [{"id": 0, "properties": [{"name": "Water"}]}],
                }
            ],
        }
    )
    assert map.open_water(0, 0)
    assert map.index(1, 0, "Back") == 0
    with pytest.raises(IndexError):
        map.index(-1, 1, "Back")


def test_border_zero_does_not_create_false_island_bubbles(maps):
    assert not any(
        (e.x, e.y, e.start) == (0, 80, 850)
        for e in bubbles.predict(metadata(27), "IslandNorth", maps["IslandNorth"])
    )


def test_frenzy_outputs_both_timelines_with_game_minimum_duration(maps):
    row = ORACLE["mountain_frenzy"]
    events = bubbles.predict(metadata(row["days"]), "Mountain", maps["Mountain"])
    branches = [e for e in events if e.start == row["start"]]
    assert {(e.x, e.y, e.kind, e.end) for e in branches} == {
        (row["x"], row["y"], "Bubbles", row["ordinary_end"]),
        (row["x"], row["y"], "Frenzy", row["frenzy_end"]),
    }
    assert all(e.scenario for e in branches)
    assert all(e.scenario is None for e in events if e.start != row["start"])


def test_beach_uses_008_probability_not_01(maps):
    row = ORACLE["beach_chance"]
    assert 0.008 < row["chance"] < 0.01
    event = next(
        e
        for e in bubbles.predict(metadata(row["days"]), "Beach", maps["Beach"])
        if e.start == row["time"]
    )
    assert (event.x, event.y, event.kind, event.scenario) == (
        row["x"],
        row["y"],
        "Bubbles",
        None,
    )


def test_early_frenzy_requires_distinct_fish_and_uses_calendar(maps):
    two = metadata(5, seed=0, fish_count=2)
    two.times_fished = 100
    assert not any(e.scenario for e in bubbles.predict(two, "Forest", maps["Forest"]))
    three = metadata(5, seed=0, fish_count=3)
    assert any(e.scenario for e in bubbles.predict(three, "Forest", maps["Forest"]))
    two.year = 2
    assert any(e.scenario for e in bubbles.predict(two, "Forest", maps["Forest"]))


def test_unknown_early_fish_count_does_not_invent_eligibility(maps):
    save = metadata(5)
    del save.fish_caught_count
    with pytest.raises(FeatureUnavailable, match="distinct fish"):
        bubbles.predict(save, "Forest", maps["Forest"])


def test_scenario_budget_fails_explicitly(maps, monkeypatch):
    monkeypatch.setattr(bubbles, "_MAX_SCENARIOS", 1)
    with pytest.raises(FeatureUnavailable, match="timelines"):
        bubbles.predict(metadata(18), "Mountain", maps["Mountain"])


def test_saved_objects_block_spawn_coordinates(maps):
    wrapped = SimpleNamespace(
        metadata=metadata(18),
        players=(),
        world=SimpleNamespace(
            locations=(
                SimpleNamespace(
                    name="Mountain", objects=(SimpleNamespace(x=82, y=40),)
                ),
            )
        ),
    )
    assert not any(
        (e.x, e.y, e.start) == (82, 40, 640)
        for e in bubbles.predict(wrapped, "Mountain", maps["Mountain"])
    )


def test_artifact_luck_matches_unmodified_farmer_daily_luck(state):
    assert ArtifactState.from_game_state(state).daily_luck == ORACLE["solo_charm_luck"]


def test_multiplayer_requires_online_set_and_uses_its_average(state):
    guest = replace(
        state.player,
        name="Guest",
        player_id=202,
        mail=frozenset(),
        has_special_charm=False,
    )
    state = replace(state, players=(state.player, guest))
    with pytest.raises(FeatureUnavailable, match="online"):
        ArtifactState.from_game_state(state)
    context = ArtifactState.from_game_state(state, online_player_indices=(0, 1))
    assert context.daily_luck == (ORACLE["solo_charm_luck"] - 0.008) / 2


def test_online_luck_preserves_game_accumulation_order(state):
    # Unmodified .NET 6 FarmerTeam.AverageDailyLuck from the inspected DLL:
    # five farmers with Special Charm, followed by one without; base -0.008.
    # Captured by outputs/game-audit/maps-average-oracle/Program.cs. Python's
    # compensated sum instead returns 0.01283333364377419 (one ULP higher).
    players = tuple(replace(state.player, player_id=i + 101) for i in range(5))
    guest = replace(
        state.player, player_id=106, mail=frozenset(), has_special_charm=False
    )
    state = replace(state, players=(*players, guest))
    context = ArtifactState.from_game_state(
        state, online_player_indices=(0, 1, 2, 3, 4, 5)
    )
    assert context.daily_luck == 0.012833333643774189


@pytest.mark.parametrize("observation", CONTEXT_ORACLE["maps"], ids=lambda m: m["name"])
def test_artifact_location_seasons_match_actual_game_maps(state, observation):
    context = ArtifactState.from_game_state(state)
    context = replace(context, save=replace(context.save, season="winter"))
    spot = ArtifactSpot(observation["name"], 1, 1)
    assert location_context(spot.location) == observation["context"]
    assert location_season(context, spot) == observation["season_in_winter"].lower()


def test_artifact_random_condition_matches_float32_game_parser(state):
    observation = CONTEXT_ORACLE["random_boundary"]
    random = SimpleNamespace(double=lambda: observation["draw"])
    assert (
        condition(
            "RANDOM " + observation["probability"],
            ArtifactState.from_game_state(state),
            ArtifactSpot("Desert", 1, 1),
            random,
        )
        is observation["result"]
    )


def test_artifact_context_override_and_map_override_remain_distinct(state):
    context = replace(
        ArtifactState.from_game_state(state),
        context_seasons={"Default": None, "Desert": "fall", "Island": "winter"},
    )
    assert location_season(context, ArtifactSpot("Desert", 1, 1)) == "fall"
    assert location_season(context, ArtifactSpot("Caldera", 1, 1)) == "summer"
    assert location_season(context, ArtifactSpot("Town", 1, 1)) == "spring"
    with pytest.raises(FeatureUnavailable, match="Desert location context"):
        location_season(
            replace(context, context_seasons={}), ArtifactSpot("Desert", 1, 1)
        )


@pytest.mark.parametrize("location", ["IslandCustom", "DesertCustom", "ModdedTown"])
def test_uninspected_artifact_context_is_not_guessed_from_its_name(
    state, artifacts, location
):
    with pytest.raises(FeatureUnavailable, match="location context"):
        artifacts.predict(
            ArtifactState.from_game_state(state), ArtifactSpot(location, 1, 1)
        )


def test_caldera_uses_journal_scraps_without_a_magnifying_glass(state, artifacts):
    context = replace(ArtifactState.from_game_state(state), mail=frozenset())
    spot = ArtifactSpot("Caldera", 1, 1)
    assert (
        artifacts.resolve("SECRET_NOTE_OR_ITEM (O)390", context, spot, Random(1))
        == "runtime:secret-note-or-stone"
    )
    assert (
        artifacts.resolve(
            "SECRET_NOTE_OR_ITEM (O)390",
            replace(context, unseen_journal=0),
            spot,
            Random(1),
        )
        == "(O)390"
    )


@pytest.mark.parametrize("indices", [(), (True,), (0, 0), (1,), (-1,), ("0",), (0, 2)])
def test_invalid_online_sets_are_rejected(state, indices):
    with pytest.raises(ValueError, match="Online player"):
        ArtifactState.from_game_state(state, online_player_indices=indices)


def test_festival_override_uses_its_own_seed_and_inactive_map_is_unavailable(
    state, artifacts
):
    row = ORACLE["festival"]
    context = ArtifactState.from_game_state(state)
    spot = ArtifactSpot("DesertFestival", row["x"], row["y"])
    active = artifacts.predict(context, spot)
    eggs = next(i for i in active.items if i.item_id == "(O)CalicoEgg")
    assert eggs.quantity == row["calico_eggs"]
    inactive = artifacts.predict(
        replace(context, save=replace(state.metadata, day=11)), spot
    )
    assert inactive.items == () and "Inactive" in inactive.note


def test_pending_mail_is_included_and_unknown_selectors_are_rejected(state):
    context = ArtifactState.from_game_state(state)
    assert condition(
        "PLAYER_HAS_MAIL Host guntherBones",
        context,
        ArtifactSpot("Town", 1, 1),
        Random(1),
    )
    with pytest.raises(ValueError, match="player selector"):
        compile_condition("PLAYER_HAS_MAIL Any guntherBones")
    with pytest.raises(ValueError, match="location selector"):
        compile_condition("LOCATION_SEASON Desert Summer")


def test_completed_notes_remove_impossible_random_alternative(state, artifacts):
    context = replace(
        ArtifactState.from_game_state(state), unseen_notes=0, unseen_journal=0
    )
    for place in ("Town", "IslandNorth"):
        assert (
            artifacts.resolve(
                "SECRET_NOTE_OR_ITEM (O)390",
                context,
                ArtifactSpot(place, 1, 1),
                Random(1),
            )
            == "(O)390"
        )


def test_missing_artifact_version_is_feature_unavailable(state):
    state = replace(state, metadata=replace(state.metadata, game_version=None))
    with pytest.raises(FeatureUnavailable, match="1.6.15"):
        ArtifactState.from_game_state(state)


def test_scenario_is_preserved_by_json_text_and_map_rows(state):
    state = replace(
        state, metadata=replace(state.metadata, days_played=18, year=1, day=18)
    )
    data = load_game_data()
    result = analyze(
        state,
        data=data,
        options=AnalysisOptions(
            progress=(),
            predictions=(),
            extras=False,
            artifacts=False,
            locations=("Mountain",),
        ),
    )
    payload = json.loads(render_json(result))
    assert any(e["scenario"] for e in payload["bubbles"])
    assert "Conditional timelines" in render_text(result, data=data)
    assert any(
        "[if " in line
        for _, _, lines in rows_for_results(result.bubbles, "bubbles")
        for line in lines
    )
