"""Regressions derived from inspected game methods, not the historical predictor.

Reference: docs/calendar-game-parity.md. Saves are synthetic; seed 390938626
is also part of the repository's original numeric/bubble reference fixtures.
"""

import json
from pathlib import Path

import pytest

from stardew.domain.numeric import SystemRandom
from stardew.domain.predictions.features.calendar_rules import (
    INSTALLED_GAME_PROFILE,
    day_random,
)
from stardew.domain.predictions.features.calico_jack import predict_calico_jack
from stardew.domain.predictions.features.crane import predict_crane
from stardew.domain.predictions.features.gem_birds import predict_gem_birds
from stardew.domain.predictions.features.mine_chests import predict_mine_chests
from stardew.domain.predictions.features.mines import predict_mines
from stardew.domain.predictions.features.night import predict_night
from stardew.domain.predictions.features.statues import predict_statues
from stardew.domain.predictions.features.trains import predict_trains
from stardew.domain.predictions.features.trash import predict_trash
from stardew.domain.predictions.features.weather import predict_green_rain
from stardew.domain.predictions.records import build_records, item_identities
from stardew.domain.predictions.records.common import RecordContext
from stardew.domain.predictions.registry import REGISTRY
from stardew.domain.predictions.report_models import ReportPredictionOptions
from stardew.domain.predictions.report_predictions import (
    _context_save,
    analyze_predictions,
)
from stardew.domain.predictions.report_support import PredictionContext
from stardew.domain.predictions.windows import calculation_offsets
from stardew.infrastructure.game_data import load_game_data
from stardew.infrastructure.saves import load_save


@pytest.fixture(scope="module")
def data():
    return load_game_data(include_maps=False)


@pytest.fixture
def saved_game(tmp_path, data):
    def create(day=123, player_fields="", root_fields=""):
        year = (day - 1) // 112 + 1
        season = ("spring", "summer", "fall", "winter")[(day - 1) // 28 % 4]
        npcs = "".join(
            f"<NPC><name>{name}</name></NPC>"
            for name in data.catalogs["predictor_characters"]
        )
        path = tmp_path / "calendar-save"
        path.write_text(
            f"""<SaveGame><uniqueIDForThisGame>390938626</uniqueIDForThisGame>
<gameVersion>1.6.15</gameVersion><year>{year}</year><currentSeason>{season}</currentSeason>
<dayOfMonth>{(day - 1) % 28 + 1}</dayOfMonth><useLegacyRandom>false</useLegacyRandom>{root_fields}
<player><name>Synthetic</name><UniqueMultiplayerID>101</UniqueMultiplayerID><gender>Male</gender>
<stats><daysPlayed>{day}</daysPlayed><trashCansChecked>100</trashCansChecked></stats>{player_fields}</player>
<locations><GameLocation><name>Town</name><characters>{npcs}</characters></GameLocation></locations></SaveGame>""",
            encoding="utf-8",
        )
        return load_save(path)

    return create


@pytest.fixture
def context(data):
    def create(day=123, count=1, **changes):
        save = {
            "gameID": 390938626,
            "version": "1.6.15",
            "daysPlayed": 123,
            "year": 2,
            "dayAdjust": 0,
            "useLegacyRandom": False,
            "dailyLuck": -0.075,
            "playerLuck": (-0.075,),
            "luckLevel": 0,
            "mp_ids": (123456789,),
            "ccComplete": True,
            "anyCcComplete": True,
            "theaterUnlocked": True,
            "hostTheaterUnlocked": True,
            "theaterBuilt": True,
            "theaterDayFirstEntered": 0,
            "quarryUnlocked": True,
            "quarryMineVisited": True,
            "deepestMineLevel": 221,
            "lowestMineLevel": 221,
            "lowestMineLevelForOrder": -1,
            "anyOnlineFarmerHasMonsterMusk": False,
            "hardmodeMines": False,
            "shuffleMineChests": "Default",
            "desertUnlocked": True,
            "anyDesertUnlocked": True,
            "hostDesertUnlocked": True,
            "hasFurnaceRecipe": True,
            "greenhouseUnlocked": True,
            "raccoonTreeFallen": True,
            "sawQiPlane": True,
            "gotCapsule": False,
            "hasMatureFairyRoseTonight": None,
            "hasGarbageBook": False,
            "trashCansChecked": (100,),
            "qiCropsActive": False,
        }
        for name in ("objects", "weapons", "boots"):
            save[name] = data.catalogs["predictor_" + name]
        save.update(changes)
        return PredictionContext(
            save, data.catalogs, count=count, day_range=(day, day + count)
        )

    return create


def rows(context, feature):
    start = context.day_range[0]
    feature(context, offset=(start - 1) // 28 * 28)
    return [facts for _, facts in context.captures]


@pytest.mark.parametrize("legacy", [False, True])
def test_day_seed_truncates_negative_odd_ids_like_csharp(legacy):
    # The expected samples were captured by calling Utility.CreateRandom in
    # the installed DLL, independently of the Python helper under test.
    vectors = json.loads(
        (Path(__file__).parents[1] / "fixtures/game-seed-boundaries.json").read_text(
            encoding="utf-8"
        )
    )
    case = next(
        case
        for case in vectors["cases"]
        if case["game_id"] == -7 and case["legacy"] == legacy
    )
    rng = day_random(
        {"gameID": case["game_id"], "useLegacyRandom": legacy},
        case["days"],
        case["a"],
        case["b"],
    )
    assert [rng.next() for _ in case["draws"]] == case["draws"]


@pytest.mark.parametrize(
    "case",
    json.loads(
        (Path(__file__).parents[1] / "fixtures/game-trash-seeds.json").read_text(
            encoding="utf-8"
        )
    )["cases"],
    ids=lambda case: f"{case['game_id']}-{'legacy' if case['legacy'] else 'hashed'}",
)
def test_trash_uses_original_day_save_seed_before_prewarming(
    context, monkeypatch, case
):
    # Captured CreateDaySaveRandom values cover a negative final legacy sum
    # and an odd ID whose / 2 rounds up if converted to double too early.
    created = []

    def random(seed):
        created.append(seed)
        return SystemRandom(seed)

    monkeypatch.setattr(
        "stardew.domain.predictions.features.trash.SystemRandom", random
    )
    saved = context(gameID=case["game_id"], useLegacyRandom=case["legacy"])
    rows(saved, predict_trash)
    assert created[0] == case["seed"]
    rng = SystemRandom(created[0])
    assert [rng.next() for _ in case["draws"]] == case["draws"]


@pytest.mark.parametrize(
    "level,name",
    [
        (10, "Leather Boots"),
        (20, "Steel Smallsword"),
        (50, "Tundra Boots"),
        (90, "Obsidian Edge"),
        (110, "Space Boots"),
    ],
)
def test_default_chests_use_fixed_game_rewards(context, level, name):
    result = rows(context(), predict_mine_chests)
    assert next(row for row in result if row["floor"] == level)["item"] == name


def test_remixed_chests_keep_the_seeded_pool(context):
    result = rows(context(shuffleMineChests="Remixed"), predict_mine_chests)
    assert result[0]["item"] == "Iron Dirk"
    assert result[0]["rewardMode"] == "Remixed"


@pytest.mark.parametrize("game_id,item_id", [(6, "(O)517"), (10, "(O)519")])
def test_remixed_rings_use_object_qualified_ids(context, game_id, item_id):
    result = rows(
        context(gameID=game_id, shuffleMineChests="Remixed"), predict_mine_chests
    )
    assert next(row for row in result if row["floor"] == 20)["item_id"] == item_id


def test_unknown_chest_mode_returns_named_alternatives(context):
    result = rows(context(shuffleMineChests=None), predict_mine_chests)[0]
    assert result["item"] is None
    assert {alternative["mode"] for alternative in result["rewardAlternatives"]} == {
        "Default",
        "Remixed",
    }
    assert result["availability"] == "original_reward_not_remaining_chest"


def test_train_rule_requires_matching_binary_profile(context):
    installed = rows(
        context(day=124, game_profile=INSTALLED_GAME_PROFILE), predict_trains
    )[0]
    fallback = rows(context(day=124), predict_trains)[0]
    assert installed["trainTime"] == 900
    assert fallback["trainTime"] == 1320
    assert installed["verification"] == "matched_installed_dll"
    assert fallback["verification"] == "unverified_historical_rule"


@pytest.mark.parametrize("profile", [None, INSTALLED_GAME_PROFILE])
def test_train_cannot_arrive_during_a_festival(context, profile):
    assert (
        rows(context(day=136, game_profile=profile), predict_trains)[0]["trainTime"]
        is None
    )


def test_new_train_chance_rejects_old_false_positive(context):
    assert (
        rows(context(day=117, game_profile=INSTALLED_GAME_PROFILE), predict_trains)[0][
            "trainTime"
        ]
        is None
    )


def test_winter_snow_is_seeded_and_not_reported_as_sun(context):
    result = rows(context(day=198), predict_green_rain)[0]
    assert result["weatherTown"] == "Snow"
    assert result["weatherAlternatives"] == ["Snow"]


def test_weather_retains_session_random_subtypes(context):
    result = rows(context(day=126), predict_green_rain)[0]
    assert result["weatherAlternatives"] == ["Rain", "Storm"]
    assert result["certainty"] == "session_dependent"


def test_saved_weather_takes_precedence_over_recalculation(context):
    result = rows(
        context(day=126, weatherOverrides={"126": "Wind"}), predict_green_rain
    )[0]
    assert result["weatherTown"] == "Wind"
    assert result["source"] == "saved"


def test_tomorrows_saved_weather_still_gets_calendar_modifications(context):
    result = rows(
        context(day=41, daysPlayed=40, weatherOverrides={"41": "Sun"}),
        predict_green_rain,
    )[0]
    assert result["weatherTown"] == "Storm"
    assert result["source"] == "calendar"


def test_current_saved_weather_was_already_resolved_by_the_game(context):
    result = rows(
        context(day=41, daysPlayed=41, weatherOverrides={"41": "Sun"}),
        predict_green_rain,
    )[0]
    assert result["weatherTown"] == "Sun"
    assert result["source"] == "saved"


def test_weather_uses_requested_day_offset(context):
    shifted = rows(context(day=197, dayAdjust=1), predict_green_rain)[0]
    assert shifted["weatherTown"] == "Snow"


@pytest.mark.parametrize("day,expected", [(48, ["Rain", "Storm"]), (96, ["Snow"])])
def test_fishing_festivals_without_map_replacements_do_not_force_sun(
    context, day, expected
):
    # PassiveFestivals has MapReplacements=null for TroutDerby and SquidFest;
    # Game1.getWeatherModificationsForDate therefore retains seeded weather.
    result = rows(context(day=day), predict_green_rain)[0]
    assert result["weatherAlternatives"] == expected
    assert result["source"] == "seeded"


def test_alternate_layout_can_remove_predicted_infestation(context):
    result = rows(context(day=130), predict_mines)[0]
    assert result["alternateLayouts"]["7"] == 60
    assert 7 not in result["infestedMonster"]
    assert 91 not in result["infestedSlime"]


def test_alternate_layout_can_create_previously_omitted_infestation(context):
    result = rows(context(day=119), predict_mines)[0]
    assert result["alternateLayouts"]["78"] == 58
    assert 78 in result["infestedMonster"]


def test_mine_progress_for_active_order_takes_precedence(context):
    result = rows(context(day=119, lowestMineLevelForOrder=20), predict_mines)[0]
    assert result["alternateLayouts"] == {}
    assert 78 not in result["infestedMonster"]


def test_alternate_layouts_were_not_available_before_164(context):
    result = rows(context(day=119, version="1.6.0"), predict_mines)[0]
    assert result["alternateLayouts"] == {}


def test_quarry_floors_require_a_previous_quarry_mine_visit(context):
    result = rows(context(day=113, quarryMineVisited=False), predict_mines)[0]
    assert result["quarryLevel"] == []


def test_quarry_area_overrides_mushroom_lighting(context):
    quarry = rows(context(day=127), predict_mines)[0]
    normal = rows(context(day=127, quarryMineVisited=False), predict_mines)[0]
    assert 106 in quarry["quarryLevel"]
    assert 106 not in quarry["rainbowLights"]
    assert 106 in normal["rainbowLights"]


def test_monster_musk_changes_the_floor_scenario(context):
    result = rows(context(day=119, anyOnlineFarmerHasMonsterMusk=True), predict_mines)[
        0
    ]
    assert result["infestedMonster"] == []
    assert result["infestedSlime"] == []


def test_unknown_monster_musk_is_a_scenario_not_an_exact_claim(context):
    result = rows(context(day=119, anyOnlineFarmerHasMonsterMusk=None), predict_mines)[
        0
    ]
    assert 78 in result["infestedMonster"]
    assert result["monsterMuskAlternative"]["monster"] == []
    assert result["dinoLevelCertainty"] == "candidates_only"
    assert not {100, 200, 300}.intersection(result["dinoLevel"])


def test_fairy_is_ineligible_on_the_morning_of_a_new_season(context):
    result = rows(context(day=28, gameID=104), predict_night)[0]
    assert "Fairy" not in result["thisEvent"]
    assert result["wakingDay"] == 29


def test_capsule_is_not_repeated_after_saved_unlock(context):
    without = rows(context(day=144, gotCapsule=False), predict_night)[0]
    already = rows(context(day=144, gotCapsule=True), predict_night)[0]
    assert "Strange Capsule" in without["thisEvent"]
    assert "Strange Capsule" not in already["thisEvent"]


def test_unknown_fairy_rose_returns_conditional_outcomes(context):
    result = rows(context(day=123, gameID=42), predict_night)[0]
    assert {candidate["event"] for candidate in result["eventCandidates"]} == {
        "Fairy",
        "(No event)",
    }
    assert result["certainty"] == "conditional"


def test_saved_night_priorities_and_wedding_override(context):
    pending = rows(
        context(day=123, pendingNightEvents=("Greenhouse repair",)), predict_night
    )[0]
    wedding = rows(
        context(day=123, pendingNightEvents=("Greenhouse repair",), weddingDays=(124,)),
        predict_night,
    )[0]
    assert pending["thisEvent"] == "Greenhouse repair"
    assert wedding["thisEvent"] == "(No event: wedding)"


def test_qi_plane_takes_priority_when_not_seen(context):
    result = rows(context(day=123, sawQiPlane=False), predict_night)[0]
    assert result["thisEvent"] == "Qi Plane"


def test_qi_bean_requires_garbage_base_chance(context):
    result = rows(context(day=123, qiCropsActive=True), predict_trash)
    assert not any(row["whichCan"] == 1 for row in result)


def test_garbage_world_unlocks_do_not_change_with_guest_flags(context):
    first = rows(context(day=123, count=28), predict_trash)
    second = rows(
        context(
            day=123,
            count=28,
            theaterUnlocked=False,
            ccComplete=False,
            desertUnlocked=False,
        ),
        predict_trash,
    )
    assert first == second


def test_desert_festival_garbage_exists_in_year_one_after_bus_unlock(context):
    result = rows(context(day=15, hostDesertUnlocked=True), predict_trash)
    festival = next(row for row in result if row["whichCan"] == 8)
    assert festival["trashItem"] == "Calico Egg"
    assert 5 <= festival["stack"] <= 8
    locked = rows(context(day=15, hostDesertUnlocked=False), predict_trash)
    assert not any(row["whichCan"] == 8 for row in locked)


def test_desert_festival_garbage_preserves_quantity_and_public_location(context, data):
    ctx = context(day=127)
    result = rows(ctx, predict_trash)
    festival = next(row for row in result if row["whichCan"] == 8)
    # After two prewarm loops, base, hat and catalogue draws, Next(5, 9) = 8.
    assert festival["stack"] == 8
    record = build_records(
        "trash", festival, RecordContext.from_prediction(ctx), item_identities(data)
    )[0]
    assert record.location == "Desert Festival"
    assert record.quantity == 8


def test_festival_statue_does_not_offer_butterfly_even_in_clear_weather(context, data):
    ctx = context(day=92)
    result = rows(ctx, predict_statues)
    assert len(result) == 1
    main = result[0]
    assert main["effectiveBlessing"] == "Fangs"
    record = build_records(
        "statue", main, RecordContext.from_prediction(ctx), item_identities(data)
    )[0]
    facts = {fact.name: fact.value for fact in record.facts}
    assert facts["blessing_clear"] == "Fangs"
    assert facts["is_festival"] is True


def test_first_cinema_visit_is_always_occupied(context):
    result = rows(context(day=123, theaterDayFirstEntered=122), predict_crane)[0]
    assert result["availability"] == "first_visit"
    assert "In Use" in result["thisEvent"]


def test_unvisited_cinema_retains_first_visit_condition(context):
    result = rows(context(day=123, theaterDayFirstEntered=-1), predict_crane)[0]
    assert result["availability"] == "conditional_first_visit"


def test_unbuilt_cinema_is_not_claimed_to_be_available(context):
    result = rows(context(day=123, theaterBuilt=False), predict_crane)[0]
    assert result["availability"] == "requires_theater"


def test_calico_super_bust_includes_payout_in_plan_and_advice(context):
    ctx = context()
    predict_calico_jack(ctx, offset=123, game_offset=153)
    result = ctx.captures[0][1]
    assert result["plan"]["hits"] == 0
    assert result["plan"]["player_total"] == 12
    assert result["plan"]["winnings_multiplier"] == 3
    assert "3x winnings" in result["advice"]


def test_calico_result_does_not_depend_on_previous_predictions(context):
    batch = context(count=154)
    predict_calico_jack(batch, offset=123)
    single = context()
    predict_calico_jack(single, offset=123, game_offset=153)
    assert batch.captures[-1] == single.captures[0]
    assert all(isinstance(row["chance"], float) for _, row in batch.captures)


def test_gem_bird_shuffle_still_produces_four_different_gems(context):
    result = rows(context(), predict_gem_birds)
    gems = [row["gems"][row["birds"][row["i"]]] for row in result]
    assert len(gems) == len(set(gems)) == 4


@pytest.mark.parametrize(
    "feature,day,expected",
    [
        ("makeover", 127, 1),
        ("makeover", 129, 1),
        ("makeover", 130, 2),
        ("winterstar", 221, 1),
        ("winterstar", 222, 2),
    ],
)
def test_default_year_selects_the_next_unfinished_festival(feature, day, expected):
    save = {"year": (day - 1) // 112 + 1, "daysPlayed": day}
    assert calculation_offsets(
        REGISTRY[feature], save, ReportPredictionOptions(), 0
    ) == (expected,)
    assert calculation_offsets(
        REGISTRY[feature], save, ReportPredictionOptions(count=2), 0
    ) == (expected, expected + 1)
    assert calculation_offsets(
        REGISTRY[feature], save, ReportPredictionOptions(start=1), 0
    ) == (0,)


@pytest.mark.parametrize("count", [None, 2])
def test_festival_in_progress_omits_past_days_but_keeps_cactus(saved_game, data, count):
    section = analyze_predictions(
        saved_game(day=128), data, ("makeover",), {"count": count}
    )[0]
    dates = {record.date.days_played for record in section.records if record.date}
    assert 127 not in dates
    assert {128, 129} <= dates
    assert any(
        record.date is None
        and dict((f.name, f.value) for f in record.facts).get("kind") == "cactus"
        for record in section.records
    )


def test_explicit_festival_year_can_still_request_historical_dates(saved_game, data):
    section = analyze_predictions(
        saved_game(day=130), data, ("makeover",), {"start": 2}
    )[0]
    assert {record.date.days_played for record in section.records if record.date} == {
        127,
        128,
        129,
    }


def test_winter_star_after_festival_uses_next_year(saved_game, data):
    section = analyze_predictions(saved_game(day=222), data, ("winterstar",))[0]
    assert {record.date.days_played for record in section.records} == {333}


@pytest.mark.parametrize("feature", ["mines", "book"])
def test_default_day_windows_start_today_even_at_month_end(saved_game, data, feature):
    section = analyze_predictions(saved_game(day=140), data, (feature,))[0]
    dates = {record.date.days_played for record in section.records if record.date}
    assert dates and all(140 <= day < 168 for day in dates)
    if feature == "mines":
        assert dates == set(range(140, 168))


def test_default_calico_games_still_use_today_and_twenty_rounds(saved_game, data):
    section = analyze_predictions(saved_game(), data, ("cj",))[0]
    assert [record.sequence for record in section.records] == list(range(1, 21))


@pytest.mark.parametrize(
    "queue,expected", [("mailbox", ()), ("mailForTomorrow", ("ccPantry",))]
)
def test_night_repairs_only_trigger_from_tomorrows_mail(
    saved_game, data, queue, expected
):
    state = saved_game(
        player_fields=f"<{queue}><string>ccPantry%&amp;NL&amp;%</string></{queue}>"
    )
    save = _context_save(state, data, ReportPredictionOptions())
    assert save["pendingNightEvents"] == expected
    assert "ccPantry" in save["hostMailWithPending"]


def test_boat_repair_uses_all_three_saved_parts_before_qi_plane(context):
    mail = ("willyBoatTicketMachine", "willyBoatHull", "willyBoatAnchor")
    repair = rows(context(hostMailWithPending=mail, sawQiPlane=False), predict_night)[0]
    finished = rows(
        context(hostMailWithPending=(*mail, "willyBoatFixed"), sawQiPlane=False),
        predict_night,
    )[0]
    assert repair["thisEvent"] == "Boat repair"
    assert finished["thisEvent"] == "Qi Plane"


def test_golden_parrot_activation_respects_saved_completion(context):
    pending = {
        "hostMailWithPending": ("activateGoldenParrotsTonight",),
        "sawQiPlane": False,
    }
    assert (
        rows(context(**pending, activatedGoldenParrot=False), predict_night)[0][
            "thisEvent"
        ]
        == "Golden Parrot activation"
    )
    assert (
        rows(context(**pending, activatedGoldenParrot=True), predict_night)[0][
            "thisEvent"
        ]
        == "Qi Plane"
    )


def test_abandoned_joja_opening_precedes_other_world_changes_on_rainy_morning(context):
    pending = {
        "hostCcCeremonySeen": True,
        "hostMailReceived": (),
        "weatherOverrides": {"124": "Rain"},
        "sawQiPlane": False,
    }
    assert (
        rows(context(**pending), predict_night)[0]["thisEvent"]
        == "Abandoned JojaMart opening"
    )
    pending["hostMailReceived"] = ("abandonedJojaMartAccessible",)
    assert rows(context(**pending), predict_night)[0]["thisEvent"] == "Qi Plane"


def test_desert_festival_without_bus_access_is_explicitly_conditional(saved_game, data):
    section = analyze_predictions(saved_game(), data, ("makeover",))[0]
    assert section.records
    for record in section.records:
        facts = {fact.name: fact.value for fact in record.facts}
        assert facts["availability"] == "requires_desert_access"
        assert "repairing the bus" in facts["conditions"]
