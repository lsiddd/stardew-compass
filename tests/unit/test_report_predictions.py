"""Historical factual parity for all 22 report predictions and public contracts."""

from dataclasses import FrozenInstanceError
from pathlib import Path
from collections.abc import Mapping
import gzip
import json

import pytest

from stardew.infrastructure.game_data import load_game_data
from stardew.infrastructure.saves import load_save
from stardew.domain.predictions import report_rules as rules
from stardew.domain.predictions.report_predictions import (
    SECTION_IDS,
    PredictionOptions,
    analyze_predictions,
    _context_save,
)
from stardew.domain.errors import FeatureUnavailable
from stardew.presentation.json import to_data

REFERENCE = json.loads(
    gzip.decompress(
        (
            Path(__file__).parents[1] / "fixtures" / "report-predictions.json.gz"
        ).read_bytes()
    )
)
CASES = REFERENCE["cases"]
FEATURES = tuple(CASES[0]["expected"])


def baseline_save(case, catalogs):
    save = {
        "gameID": case["game_id"],
        "version": case["version"],
        "daysPlayed": 156,
        "year": 2,
        "dayAdjust": 0,
        "seasonNames": ["Spring", "Summer", "Fall", "Winter"],
        "dayNames": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        "mp_ids": case["player_ids"],
        "names": ["Alice", "Bob"][: len(case["player_ids"])],
        "gender": ["Female", "Male"][: len(case["player_ids"])],
        "deepestMineLevel": 120,
        "timesFedRaccoons": 5,
        "dailyLuck": -0.1,
        "luckLevel": 0,
        "canHaveChildren": False,
        "quarryUnlocked": True,
        "desertUnlocked": True,
        "greenhouseUnlocked": True,
        "theaterUnlocked": True,
        "ccComplete": True,
        "jojaComplete": False,
        "hasFurnaceRecipe": True,
        "hasSpecialCharm": False,
        "leoMoved": False,
        "hasGarbageBook": False,
        "gotMysteryBook": False,
        "useLegacyRandom": case["legacy"],
        "hardmodeMines": False,
        "qiCropsActive": False,
        "visitsUntilY1Guarantee": -1,
        "originalGuarantee": -1,
    }
    for key, value in (
        ("geodesCracked", 10),
        ("mysteryBoxesOpened", 10),
        ("ticketPrizesClaimed", 10),
        ("timesEnchanted", 2),
        ("trashCansChecked", 100),
    ):
        save[key] = [value] * len(case["player_ids"])
    names = {
        "cartItems": "cart_items_legacy",
        "cartItems_1_4": "cart_items_14",
        "cartFurniture": "cart_furniture",
        "geodeContents": "geode_contents",
        "wallpaperEquiv": "wallpaper_equivalents",
        "weapons": "weapons",
        "boots": "boots",
        "objects": "objects",
        "furniture": "furniture",
        "shirts": "shirts",
        "characters": "characters",
        "donatedItems": "donated_items",
    }
    for old, catalog in names.items():
        save[old] = rules.deepcopy(catalogs["predictor_" + catalog])
    if rules.compare_version(case["version"], "1.6") >= 0:
        save["geodeContents"]["275"].append("_Book_Artifact")
    return save


def canonical(value):
    if isinstance(value, Mapping):
        return {str(key): canonical(child) for key, child in value.items()}
    if isinstance(value, (tuple, list)):
        return [canonical(child) for child in value]
    return value


def historical_projection(value, feature):
    rows = canonical(value)
    for _, facts in rows:
        facts.pop("itemIDs", None)
        facts.pop("item_id", None)
        if isinstance(facts.get("item"), dict):
            facts["item"].pop("item_id", None)
        # Dates were previously table headings; compare them in API tests below.
        if feature == "predict_cart":
            facts.pop("day", None)
            facts.pop("startDay", None)
    return rows


@pytest.mark.parametrize(
    "case",
    CASES,
    ids=lambda x: (
        f"{x['version']}_{x['game_id']}_{'legacy' if x['legacy'] else 'hashed'}"
    ),
)
@pytest.mark.parametrize("feature", FEATURES)
def test_all_prediction_calculations_match_historical_facts(case, feature):
    catalogs = load_game_data().catalogs
    context = rules.PredictionContext(baseline_save(case, catalogs), catalogs, count=3)
    getattr(rules, feature)(context)
    assert historical_projection(context.captures, feature) == historical_projection(
        case["expected"][feature], feature
    )


@pytest.fixture
def game(tmp_path):
    data = load_game_data()
    names = data.catalogs["predictor_characters"]
    stats = "".join(
        f"<item><key><string>{key}</string></key><value><unsignedInt>{value}</unsignedInt></value></item>"
        for key, value in (
            ("daysPlayed", 156),
            ("geodesCracked", 442),
            ("MysteryBoxesOpened", 10),
            ("timesEnchanted", 2),
            ("ticketPrizesClaimed", 5),
            ("trashCansChecked", 100),
        )
    )
    npcs = "".join(f"<NPC><name>{name}</name></NPC>" for name in names)
    player = f"<name>Alice</name><gender>Female</gender><UniqueMultiplayerID>123456789012345678</UniqueMultiplayerID><stats><Values>{stats}</Values></stats><mailReceived><string>ccCraftsRoom</string><string>ccVault</string><string>ccPantry</string></mailReceived><deepestMineLevel>120</deepestMineLevel>"
    path = tmp_path / "save"
    path.write_text(
        f"<SaveGame><uniqueIDForThisGame>123456789</uniqueIDForThisGame><gameVersion>1.6.15</gameVersion><year>2</year><dayOfMonth>16</dayOfMonth><currentSeason>summer</currentSeason><dailyLuck>0.1</dailyLuck><player>{player}</player><locations><GameLocation><name>Town</name><characters>{npcs}</characters></GameLocation></locations></SaveGame>"
    )
    return load_save(path), data


def test_all_22_public_sections_and_immutable_results(game):
    state, data = game
    result = analyze_predictions(state, data)
    assert tuple(section.section_id for section in result) == SECTION_IDS
    assert all(section.available and section.records for section in result)
    with pytest.raises(FrozenInstanceError):
        result[0].section_id = "changed"
    assert "<" not in json.dumps(to_data(result[15]))


def test_calls_section_order_and_rendering_do_not_change_facts(game):
    state, data = game
    options = PredictionOptions(start=443, count=2)
    first = analyze_predictions(state, data, ("geode", "mystery"), options)
    assert first == analyze_predictions(state, data, ("geode", "mystery"), options)
    reversed_result = analyze_predictions(state, data, ("mystery", "geode"), options)
    assert first[0] == reversed_result[1]
    assert first[1] == reversed_result[0]
    assert data.catalogs["predictor_geode_contents"]["275"].count("_Book_Artifact") == 0


@pytest.mark.parametrize(
    "section",
    ["mines", "train", "night", "crane", "greenrain", "statue", "sandy", "wallpaper"],
)
def test_explicit_dates_span_all_requested_pages(game, section):
    state, data = game
    records = analyze_predictions(
        state, data, (section,), PredictionOptions(start=1, count=56)
    )[0].records
    assert {record.date.days_played for record in records} == set(range(1, 57))


def test_bookseller_dates_and_stock_prices_are_structured(game):
    state, data = game
    result = analyze_predictions(
        state, data, ("book",), PredictionOptions(start=1, count=56)
    )[0]
    dates = {record.date.days_played for record in result.records}
    assert (
        len(dates) == 4
        and any(date <= 28 for date in dates)
        and any(date > 28 for date in dates)
    )
    assert all(
        record.item_name and record.price in (5000, 8000, 10000, 15000, 20000)
        for record in result.records
    )


def test_exact_shirt_and_common_stone_ids(game):
    state, data = game
    sandy = analyze_predictions(state, data, ("sandy",))[0]
    assert all(
        record.item_id
        == f"(S){next(f.value for f in record.facts if f.name == 'num_i_d')}"
        for record in sandy.records
    )
    geodes = analyze_predictions(
        state, data, ("geode",), PredictionOptions(start=443, count=1)
    )[0]
    assert all(
        record.item_id == "(O)390"
        for record in geodes.records
        if record.item_name == "Stone"
    )
    assert all(record.item_id is not None for record in geodes.records)


def test_festival_dates_player_specific_cactus_and_named_outfits(game):
    state, data = game
    records = analyze_predictions(state, data, ("makeover",))[0].records
    racing = [
        record
        for record in records
        if any(fact.name == "racers" for fact in record.facts)
    ]
    assert [record.date.days_played for record in racing] == [127, 128, 129]
    cactus = [
        record
        for record in records
        if any(fact.name == "kind" and fact.value == "cactus" for fact in record.facts)
    ]
    assert cactus[0].player_id == state.player.player_id
    outfits = [
        record
        for record in records
        if any(fact.name == "outfit" for fact in record.facts)
    ]
    assert len(outfits) == 3
    assert all(record.date.days_played in (127, 128, 129) for record in outfits)
    assert all(
        isinstance(next(f.value for f in record.facts if f.name == "outfit"), Mapping)
        for record in outfits
    )


def test_report_luck_defaults_are_independent_of_saved_luck(game):
    state, data = game
    assert _context_save(state, data, PredictionOptions())["dailyLuck"] == -0.1
    assert (
        _context_save(state, data, PredictionOptions(daily_luck=0.05))["dailyLuck"]
        == 0.05
    )


def test_missing_feature_requirements_are_explicit(game, tmp_path):
    state, data = game
    path = tmp_path / "old"
    path.write_text(state.source.read_text().replace("1.6.15", "1.4"))
    old = load_save(path)
    with pytest.raises(FeatureUnavailable, match="1.6"):
        analyze_predictions(old, data, ("mystery",))
    complete = analyze_predictions(old, data)
    assert not next(
        section for section in complete if section.section_id == "mystery"
    ).available


def test_wallpaper_records_preserve_shop_availability_and_texture_ids(game):
    state, data = game
    records = analyze_predictions(
        state, data, ("wallpaper",), PredictionOptions(start=1, count=7)
    )[0].records
    assert all(record.location in ("Pierre", "JojaMart") for record in records)
    assert all(
        any(f.name == "texture_id" and isinstance(f.value, int) for f in record.facts)
        for record in records
        if record.item_name
    )
    wednesday = [
        record
        for record in records
        if record.location == "Pierre" and record.date.days_played == 3
    ]
    assert len(wednesday) == 1 and wednesday[0].facts[0].value is False


def test_raccoon_requests_are_individual_quantified_records_with_seasonal_choices(game):
    state, data = game
    records = analyze_predictions(
        state, data, ("raccoon",), PredictionOptions(start=1, count=2)
    )[0].records
    assert len(records) == 6
    assert {record.sequence for record in records} == {1, 2}
    assert all(record.quantity is not None for record in records)
    assert any(len(record.alternatives) == 4 for record in records)
    assert all(alt.item_id for record in records for alt in record.alternatives)


def test_count_only_sequence_starts_after_saved_counter(game):
    state, data = game
    records = analyze_predictions(state, data, ("geode",), PredictionOptions(count=2))[
        0
    ].records
    assert {record.sequence for record in records} == {443, 444}


def test_mines_intervals_preserve_full_calendar_facts_and_reduce_work(
    game, monkeypatch
):
    from stardew.domain.predictions import report_calendar

    state, data = game
    generator = report_calendar.SystemRandom
    calls = []

    def counted_generator(seed):
        calls.append(seed)
        return generator(seed)

    monkeypatch.setattr(report_calendar, "SystemRandom", counted_generator)
    reference = analyze_predictions(
        state, data, ("mines",), PredictionOptions(start=1, count=56)
    )[0].records
    full_calls = len(calls)
    for start, count in ((1, 1), (28, 3), (56, 1)):
        calls.clear()
        selected = analyze_predictions(
            state, data, ("mines",), PredictionOptions(start=start, count=count)
        )[0].records
        assert selected == tuple(
            record
            for record in reference
            if start <= record.date.days_played < start + count
        )
        assert len(calls) < full_calls / 2


def test_prediction_options_freeze_player_indices_and_reject_fractional_intervals():
    indices = [0, 1]
    options = PredictionOptions(player_indices=indices)
    indices.append(2)
    assert options.player_indices == (0, 1)
    with pytest.raises(TypeError, match="count"):
        PredictionOptions(count=1.5)
