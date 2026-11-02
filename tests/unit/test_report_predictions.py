"""Historical compatibility where valid, plus public prediction contracts.

The frozen reference is the previous predictor, not an oracle for the game.
Explicitly invalidated cases retain their old bytes and a specific skip reason;
independent game-rule tests cover the corrected behavior.
"""

import gzip
import json
from collections.abc import Mapping
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from stardew.domain.errors import FeatureUnavailable
from stardew.domain.predictions import report_rules as rules
from stardew.domain.predictions.report_predictions import (
    SECTION_IDS,
    PredictionOptions,
    _context_save,
    analyze_predictions,
)
from stardew.infrastructure.game_data import load_game_data
from stardew.infrastructure.saves import load_save
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
        "lowestMineLevel": 120,
        "shuffleMineChests": "Remixed",
        "timesFedRaccoons": 5,
        "dailyLuck": -0.1,
        "luckLevel": 0,
        "canHaveChildren": False,
        "gotCapsule": False,
        "sawQiPlane": True,
        "raccoonTreeFallen": True,
        "hasMatureFairyRoseTonight": False,
        "quarryUnlocked": True,
        "quarryMineVisited": True,
        "desertUnlocked": True,
        "greenhouseUnlocked": True,
        "theaterUnlocked": True,
        "theaterBuilt": True,
        "theaterDayFirstEntered": 0,
        "ccComplete": True,
        "jojaComplete": False,
        "hasFurnaceRecipe": True,
        "hasSpecialCharm": False,
        "leoMoved": False,
        "hasGarbageBook": False,
        "gotMysteryBook": False,
        "useLegacyRandom": case["legacy"],
        "hardmodeMines": False,
        "anyOnlineFarmerHasMonsterMusk": False,
        "qiCropsActive": False,
        "goldenCoconutCracked": True,
        "hasGoldenCoconutHat": True,
        "hasArtifactFound": True,
        "fishingLevel": 10,
        "hasFarmingMastery": False,
        "houseUpgradeLevel": 0,
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
    # Identity, provenance and explicit uncertainty were absent from the old
    # capture format. Their public contracts have separate rule/API tests.
    additional_fields = {
        "predict_geodes": ("dropAlternatives", "openingRule"),
        "predict_mystery_boxes": (
            "requiresFishingLevel",
            "farmingMasteryRequired",
            "matchesSavedMastery",
            "seedResult",
            "dropAlternatives",
            "certainty",
            "openingRule",
        ),
        "predict_prize_ticket": ("seedAlternatives", "conditions"),
        "predict_trains": ("ruleProfile", "verification"),
        "predict_mine_chests": (
            "rewardMode",
            "rewardAlternatives",
            "availability",
            "availabilityCondition",
        ),
        "predict_green_rain": (
            "weatherAlternatives",
            "certainty",
            "source",
            "assumptions",
        ),
        "predict_night": ("wakingDay", "eventCandidates", "certainty", "conditions"),
        "predict_mines": (
            "dinoLevelCertainty",
            "dinoLevelConditions",
            "alternateLayouts",
            "monsterMusk",
            "monsterMuskAlternative",
            "assumptions",
        ),
        "predict_statues": (
            "isFestival",
            "effectiveBlessing",
            "weatherAlternatives",
            "weatherSource",
            "conditions",
            "spawnConditions",
        ),
        "predict_calico_jack": ("plan", "conditions"),
        "predict_crane": (
            "availability",
            "availabilityIfBuilt",
            "theaterBuilt",
            "conditions",
        ),
        "predict_trash": ("conditions",),
    }
    rows = canonical(value)
    for _, facts in rows:
        for field in additional_fields.get(feature, ()):
            facts.pop(field, None)
        facts.pop("itemIDs", None)
        facts.pop("item_id", None)
        if isinstance(facts.get("item"), dict):
            facts["item"].pop("item_id", None)
        # Dates were previously table headings; compare them in API tests below.
        if feature == "predict_cart":
            facts.pop("day", None)
            facts.pop("startDay", None)
        # Historical snapshots retained a previous iteration's locals. Normalize
        # those two corrected fields; public regression tests assert their values.
        if feature == "predict_trash":
            facts.pop("stack", None)
        if feature == "predict_calico_jack" and facts.get("chance") is None:
            # The old local was unset until a dealer branch used it. The fixed
            # fixture luck (-0.1, level 0) implies the game's 0.0005 minimum.
            facts["chance"] = 0.0005
        if feature in ("predict_night", "predict_crane"):
            facts["thisEvent"] = facts["thisEvent"].strip()
        if feature == "predict_trains" and "Train at" not in facts.get("thisTrain", ""):
            facts["trainTime"] = None
    return rows


def historical_invalidation(case, feature):
    """Identify audited defects, never infer invalidation from actual output."""
    universal = {
        "predict_raccoon": (
            "Historical reward four has seven Fairy Dust instead of five, and "
            "weighted request pools allowed duplicate item IDs; see test_loot_game_rules."
        ),
        "predict_green_rain": (
            "Historical weather claimed a definite Rain subtype and omitted "
            "calendar overrides; see test_calendar_game_rules."
        ),
        "predict_makeover": (
            "Historical cactus used the game ID instead of the player's seed, "
            "and festival selection missed eligibility/draw rules; see test_game_seed_rules."
        ),
    }
    if feature in universal:
        return universal[feature]
    negative_legacy = case["game_id"] == -123456789 and case["legacy"]
    large_hashed = case["game_id"] == 9223372036854775807 and not case["legacy"]
    if feature == "predict_statues":
        if negative_legacy:
            return (
                "Historical statue seeds floored a negative odd game ID instead of "
                "C# integer division toward zero; see test_calendar_game_rules."
            )
        return (
            "Historical statue emitted butterfly coordinates even on guaranteed "
            "rain days; see test_calendar_game_rules."
        )
    if feature == "predict_trains" and not large_hashed:
        if negative_legacy:
            return (
                "Historical train seeds used fractional division/flooring for a "
                "negative legacy game ID; see test_calendar_game_rules."
            )
        return (
            "Historical trains ran on a festival day (Luau or Moonlight Jellies); "
            "see test_calendar_game_rules."
        )
    if case["version"] in ("1.6", "1.6.15"):
        modern = {
            "predict_enchantments": (
                "Historical enchantment seed took an exact integer remainder before "
                "the game's double conversion; see test_game_seed_rules."
            ),
            "predict_winter_star": (
                "Historical Winter Star used the wrong large-player-ID conversion "
                "and donor filtering; see test_game_seed_rules."
            ),
            "predict_mines": (
                "Historical mine candidates included forced Skull Cavern chest floors "
                "and omitted eligible alternate layouts; see test_calendar_game_rules."
            ),
            "predict_night": (
                "Historical night events omitted Fairy Rose alternatives and one-time "
                "world-state gates; see test_calendar_game_rules."
            ),
        }
        if feature in modern:
            return modern[feature]
    if negative_legacy and feature in {
        "predict_bookseller",
        "predict_cart",
        "predict_geodes",
        "predict_krobus",
        "predict_mystery_boxes",
        "predict_sandy",
        "predict_wallpaper",
        "predict_trash",
    }:
        return (
            "Historical negative legacy seed used fractional division/flooring "
            "instead of C# integer division and truncation; see test_loot_game_rules "
            "and test_game_seed_rules."
        )
    if large_hashed and feature == "predict_mine_chests":
        return (
            "Historical remixed chest multiplied an exact Int64; the game converts "
            "to double before multiplying by 512; see test_calendar_game_rules."
        )
    return None


def historical_parameters():
    for case in CASES:
        for feature in FEATURES:
            reason = historical_invalidation(case, feature)
            yield pytest.param(
                case,
                feature,
                id=f"{feature}-{case['version']}_{case['game_id']}_{'legacy' if case['legacy'] else 'hashed'}",
                marks=pytest.mark.skip(reason=reason) if reason else (),
            )


@pytest.mark.parametrize("case,feature", tuple(historical_parameters()))
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
    player = f"<name>Alice</name><gender>Female</gender><UniqueMultiplayerID>123456789012345678</UniqueMultiplayerID><stats><Values>{stats}</Values></stats><mailReceived><string>ccCraftsRoom</string><string>ccVault</string><string>ccPantry</string><string>VisitedQuarryMine</string></mailReceived><deepestMineLevel>120</deepestMineLevel>"
    path = tmp_path / "save"
    path.write_text(
        f"<SaveGame><uniqueIDForThisGame>123456789</uniqueIDForThisGame><gameVersion>1.6.15</gameVersion><year>2</year><dayOfMonth>16</dayOfMonth><currentSeason>summer</currentSeason><dailyLuck>0.1</dailyLuck><mine_lowestLevelReached>120</mine_lowestLevelReached><player>{player}</player><locations><GameLocation><name>Town</name><characters>{npcs}</characters></GameLocation></locations></SaveGame>"
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
    assert [record.date.days_played for record in racing] == [239, 240, 241]
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
    assert all(record.date.days_played in (239, 240, 241) for record in outfits)
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
    path.write_text(state.source.read_text(encoding="utf-8").replace("1.6.15", "1.4"))
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
    from stardew.domain.predictions.features import calendar_rules as report_calendar

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
    assert full_calls > 0
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
