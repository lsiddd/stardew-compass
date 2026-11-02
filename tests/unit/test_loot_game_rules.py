"""Game-rule regressions from the installed Stardew 1.6.15 assembly.

The seed vector was captured from Utility.CreateRandomSeed in the unmodified
DLL (SHA-256 f3e97f01d3fd2b1e6094fc8d2b59950aa6cb9d6cd1bf1b39d72d58edda8aad12).
Other cases exercise branches inspected in GeodeMenu, Utility, Raccoon,
PrizeTicketMenu, ShopBuilder and ItemQueryResolver, with synthetic saved state.
No game installation, decompiler or private save is required to run these tests.
"""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from stardew.api import ReportPredictionOptions, load_game_data, load_save
from stardew.domain.predictions.features.shop_selection import (
    get_random_items,
    get_random_wall_floor,
)
from stardew.domain.predictions.loot.seeds import player_sequence_seed
from stardew.domain.predictions.report_predictions import analyze_predictions
from stardew.domain.predictions.report_support import PredictionContext


@pytest.fixture
def data():
    return load_game_data(include_maps=False)


@pytest.fixture
def save_factory(tmp_path):
    def create(
        *,
        game_id=390938626,
        player_id=101,
        coconut=True,
        artifact=True,
        artifact_pending=False,
        fishing=10,
        mastery=0,
        house=1,
        guarantee=-1,
    ):
        path = tmp_path / "synthetic.xml"
        received = "<string>artifactFound</string>" if artifact else ""
        pending = (
            "<string>artifactFound%&amp;NL&amp;%</string>" if artifact_pending else ""
        )
        level = f"<fishingLevel>{fishing}</fishingLevel>" if fishing is not None else ""
        path.write_text(
            f"""<SaveGame><uniqueIDForThisGame>{game_id}</uniqueIDForThisGame>
<gameVersion>1.6.15</gameVersion><year>1</year><currentSeason>spring</currentSeason>
<dayOfMonth>1</dayOfMonth><useLegacyRandom>false</useLegacyRandom>
<goldenCoconutCracked>{str(coconut).lower()}</goldenCoconutCracked>
<visitsUntilY1Guarantee>{guarantee}</visitsUntilY1Guarantee>
<player><name>Test Farmer</name><UniqueMultiplayerID>{player_id}</UniqueMultiplayerID>
<deepestMineLevel>120</deepestMineLevel>{level}<houseUpgradeLevel>{house}</houseUpgradeLevel>
<stats><daysPlayed>1</daysPlayed><geodesCracked>0</geodesCracked><Values>
<item><key><string>mastery_0</string></key><value><unsignedInt>{mastery}</unsignedInt></value></item>
</Values></stats><mailReceived>{received}<string>goldenCoconutHat</string></mailReceived>
<mailForTomorrow>{pending}</mailForTomorrow></player></SaveGame>""",
            encoding="utf-8",
        )
        return load_save(path)

    return create


def records(state, data, section, start, count=1):
    return analyze_predictions(
        state, data, (section,), ReportPredictionOptions(start=start, count=count)
    )[0].records


def facts(record):
    return {fact.name: fact.value for fact in record.facts}


def container(rows, name):
    return next(row for row in rows if facts(row)["container"] == name)


@pytest.mark.parametrize("legacy", [False, True])
def test_next_twenty_geodes_match_original_game_dll(save_factory, data, legacy):
    fixture = json.loads(
        (Path(__file__).parents[1] / "fixtures/game-geode-results.json").read_text()
    )
    state = save_factory(game_id=fixture["game_id"], player_id=fixture["player_id"])
    state = replace(
        state,
        metadata=replace(state.metadata, use_legacy_random=legacy),
        players=(
            replace(state.player, deepest_mine_level=fixture["deepest_mine_level"]),
        ),
    )
    names = dict(
        zip(
            (
                "Geode",
                "Frozen Geode",
                "Magma Geode",
                "Omni Geode",
                "Artifact Trove",
                "Golden Coconut",
            ),
            ("535", "536", "537", "749", "275", "791"),
            strict=True,
        )
    )
    actual = {
        (row.sequence, names[facts(row)["container"]]): (row.item_id, row.quantity)
        for row in records(state, data, "geode", 468, count=20)
    }
    expected = {
        (row["sequence"], row["container"]): (row["item_id"], row["quantity"])
        for row in fixture["cases"]
        if row["legacy"] == legacy
    }
    assert len(expected) == 120
    assert actual == expected


@pytest.mark.parametrize("legacy,expected", [(False, -2029016984), (True, 0)])
def test_geode_seed_matches_game_integer_division_before_double(legacy, expected):
    save = {"gameID": 1, "mp_ids": [-3], "useLegacyRandom": legacy}
    assert player_sequence_seed(save, 1, 0) == expected


def test_first_golden_coconut_uses_clint_override(save_factory, data):
    state = save_factory(coconut=False)
    result = container(records(state, data, "geode", 468), "Golden Coconut")
    assert (result.item_id, result.quantity) == ("(O)73", 1)
    assert "First Golden Coconut" in facts(result)["opening_rule"]
    assert result.alternatives == ()


@pytest.mark.parametrize(
    "artifact,pending,expected",
    [(False, False, "(O)390"), (False, True, "(O)122"), (True, False, "(O)122")],
)
def test_clint_replaces_artifacts_only_before_received_or_pending_mail(
    save_factory, data, artifact, pending, expected
):
    state = save_factory(artifact=artifact, artifact_pending=pending)
    result = container(records(state, data, "geode", 21), "Magma Geode")
    assert result.item_id == expected
    assert result.quantity == (5 if expected == "(O)390" else 1)


def test_artifact_trove_is_exempt_from_first_artifact_override(save_factory, data):
    state = save_factory(artifact=False)
    result = container(records(state, data, "geode", 2), "Artifact Trove")
    assert (result.item_id, result.quantity) == ("(O)123", 1)


@pytest.mark.parametrize("sequence,quantity", [(11, 1), (28, 5)])
def test_qi_bean_quantity_uses_seeded_geode_roll(
    save_factory, data, sequence, quantity
):
    state = save_factory()
    before = container(records(state, data, "geode", sequence), "Geode")
    beans = next(value for value in before.alternatives if value.item_id == "(O)890")
    assert beans.quantity == quantity
    assert "session RNG" not in beans.condition
    active = replace(state, world=replace(state.world, qi_crops_active=True))
    result = container(records(active, data, "geode", sequence), "Geode")
    assert (result.item_id, result.quantity) == ("(O)890", quantity)


def test_first_coconut_overrides_even_qi_bean_drop(save_factory, data):
    state = save_factory(coconut=False)
    state = replace(state, world=replace(state.world, qi_crops_active=True))
    result = container(records(state, data, "geode", 28), "Golden Coconut")
    assert (result.item_id, result.quantity) == ("(O)73", 1)


@pytest.mark.parametrize(
    "fishing,expected,quantity", [(5, "(O)242", 2), (6, "(O)687", 1), (10, "(O)687", 1)]
)
def test_mystery_box_respects_unmodified_fishing_level(
    save_factory, data, fishing, expected, quantity
):
    state = save_factory(fishing=fishing)
    result = container(
        records(state, data, "mystery", 39),
        "Golden Mystery Box without Farming Mastery",
    )
    assert (result.item_id, result.quantity) == (expected, quantity)
    assert result.alternatives == ()


def test_unknown_fishing_level_retains_explicit_alternative(save_factory, data):
    state = save_factory(fishing=None)
    result = container(
        records(state, data, "mystery", 39),
        "Golden Mystery Box without Farming Mastery",
    )
    assert facts(result)["requires_fishing_level"] == 6
    assert [(value.item_id, value.quantity) for value in result.alternatives] == [
        ("(O)242", 2)
    ]


@pytest.mark.parametrize("mastery", [0, 1])
def test_golden_box_columns_identify_farming_mastery(save_factory, data, mastery):
    rows = records(save_factory(mastery=mastery), data, "mystery", 15)
    without = container(rows, "Golden Mystery Box without Farming Mastery")
    with_mastery = container(rows, "Golden Mystery Box with Farming Mastery")
    assert facts(without)["matches_saved_mastery"] is (mastery == 0)
    assert facts(with_mastery)["matches_saved_mastery"] is (mastery > 0)
    assert not any("Foraging" in facts(row)["container"] for row in rows)


@pytest.mark.parametrize(
    "house,expected",
    [
        (0, "(F)BluePinstripeBed"),
        (1, "(F)BluePinstripeDoubleBed"),
        (3, "(F)BluePinstripeDoubleBed"),
    ],
)
def test_prize_six_uses_current_house_upgrade(save_factory, data, house, expected):
    result = records(save_factory(house=house), data, "prize", 6)[0]
    assert result.item_id == expected


@pytest.mark.parametrize(
    "request_number,season,expected",
    [
        (8, "fall", "Pickled Eggplant"),
        (10, "fall", "Pickled Pumpkin"),
        (20, "winter", "Powdermelon Jelly"),
    ],
)
def test_raccoon_preserves_pool_weights_but_rejects_same_item(
    save_factory, data, request_number, season, expected
):
    second = next(
        row
        for row in records(save_factory(), data, "raccoon", request_number)
        if facts(row)["slot"] == 2
    )
    selected = next(
        value
        for value in second.alternatives
        if value.condition == f"Request season fixed at activation: {season}"
    )
    assert selected.item_name == expected


def test_fourth_raccoon_reward_is_five_fairy_dust(save_factory, data):
    reward = next(
        row
        for row in records(save_factory(), data, "raccoon", 4)
        if facts(row)["role"] == "reward"
    )
    assert (reward.item_id, reward.quantity) == ("(O)872", 5)


@pytest.mark.parametrize("day,price", [(20, 120), (48, 270), (265, 160)])
def test_krobus_synced_bread_seed_contains_save_id(save_factory, data, day, price):
    result = records(save_factory(), data, "krobus", day)[0]
    assert (result.item_id, result.quantity, result.price) == ("(O)216", 5, price)


def test_cart_guarantee_deduplicates_before_consuming_stock_draws(save_factory, data):
    state = save_factory(game_id=98, guarantee=3)
    with_guarantee = records(state, data, "cart", 12)
    no_guarantee = replace(
        state, world=replace(state.world, visits_until_y1_guarantee=-1)
    )
    assert with_guarantee == records(no_guarantee, data, "cart", 12)
    cabbage = [row for row in with_guarantee if row.item_id == "(O)485"]
    assert [(row.price, row.quantity) for row in cabbage] == [(500, 5)]


class EqualPriorities:
    def __init__(self):
        self.calls = 0

    def next(self):
        self.calls += 1
        return 7


def test_shop_sort_keeps_equal_priorities_and_catalog_order():
    pool = {
        "_2": {"id": "2", "price": 1, "offlimits": False},
        "_1": {"id": "1", "price": 1, "offlimits": False},
        "_3": {"id": "3", "price": 0, "offlimits": False},
    }
    rng = EqualPriorities()
    context = PredictionContext({"objects": pool}, {})
    assert get_random_items(context, rng, "objects", 1, 3, True, True, how_many=3) == [
        "_2",
        "_1",
    ]
    assert rng.calls == 3


def test_wallpaper_sort_keeps_ties_and_draws_for_excluded_items():
    rng = EqualPriorities()
    context = PredictionContext({}, {})
    assert get_random_wall_floor(context, rng, 0, 3, 2, {"1": True}, 3) == [0, 2, 3]
    assert rng.calls == 6


ENCHANTMENT_REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/game-enchantment-rules.json").read_text()
)


def saved_tool(save_factory, *, kind, level, history="fresh", legacy=False):
    state = save_factory(
        game_id=ENCHANTMENT_REFERENCE["game_id"],
        player_id=ENCHANTMENT_REFERENCE["player_id"],
    )
    current_type = (
        "BottomlessEnchantment" if kind == "WateringCan" else "GenerousEnchantment"
    )
    current_name = "Bottomless" if kind == "WateringCan" else "Generous"
    older_name = "Efficient" if kind == "WateringCan" else "Archaeologist"
    current = (
        ""
        if history in ("fresh", "missing")
        else f'<BaseEnchantment xsi:type="{current_type}" />'
    )
    previous = "" if history == "fresh" else f"<string>{current_name}</string>"
    if history == "two_previous":
        previous += f"<string>{older_name}</string>"
    history_xml = (
        '<previousEnchantments xsi:nil="true" />'
        if history == "missing"
        else f"<previousEnchantments>{previous}</previousEnchantments>"
    )
    upgrade = "" if level is None else f"<upgradeLevel>{level}</upgradeLevel>"
    item = f'''<items><Item xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="{kind}">
<itemId>{kind}</itemId><name>Probe Tool</name>{upgrade}
<enchantments>{current}</enchantments>{history_xml}</Item></items>'''
    text = state.source.read_text().replace("</player>", item + "</player>")
    if legacy:
        text = text.replace("<useLegacyRandom>false", "<useLegacyRandom>true")
    state.source.write_text(text)
    return load_save(state.source)


@pytest.mark.parametrize(
    "case",
    ENCHANTMENT_REFERENCE["cases"],
    ids=lambda case: (
        f"{case['kind']}-{case['level']}-{case['history']}-{'legacy' if case['legacy'] else 'hashed'}"
    ),
)
def test_saved_tool_enchantments_match_unmodified_game_methods(
    save_factory, data, case
):
    state = saved_tool(
        save_factory,
        kind=case["kind"],
        level=case["level"],
        history=case["history"],
        legacy=case["legacy"],
    )
    result = next(
        row
        for row in records(state, data, "enchant", 1)
        if facts(row).get("tool_slot") == 1
    )
    aliases = {"Expansive": "Reaching", "Auto-Hook": "Auto Hook"}
    expected_pool = tuple(aliases.get(name, name) for name in case["pool"])
    assert facts(result)["eligible_enchantments"] == expected_pool
    assert result.item_name == aliases.get(case["selected"], case["selected"])
    assert facts(result)["certainty"] == "saved_tool_state"
    assert facts(result)["scenario"] == "saved_inventory_tool"


@pytest.mark.parametrize("level,history", [(None, "fresh"), (4, "missing")])
def test_saved_tool_missing_data_does_not_claim_exact_enchantment(
    save_factory, data, level, history
):
    state = saved_tool(save_factory, kind="Hoe", level=level, history=history)
    rows = records(state, data, "enchant", 1)
    exact = next(row for row in rows if facts(row).get("tool_slot") == 1)
    generic = next(
        row
        for row in rows
        if facts(row).get("tool") == "Hoe" and "fresh_enchantment" in facts(row)
    )
    assert exact.item_name is None
    assert facts(exact)["certainty"] == "missing_tool_state"
    assert facts(generic)["scenario"] == "new_iridium_tool_without_history"
    assert any("below iridium" in alt.condition for alt in generic.alternatives)


def test_saved_history_internal_names_and_snapshot_scope(save_factory, data):
    state = saved_tool(
        save_factory, kind="WateringCan", level=4, history="two_previous"
    )
    state.source.write_text(
        state.source.read_text().replace(
            "<string>Efficient</string>", "<string>Expansive</string>"
        )
    )
    state = load_save(state.source)
    rows = [
        row
        for row in records(state, data, "enchant", 1, 2)
        if facts(row).get("tool_slot") == 1
    ]
    assert [row.item_name for row in rows] == ["Efficient", "Efficient"]
    assert all(
        facts(row)["previous_enchantments"] == ("Bottomless", "Reaching")
        for row in rows
    )
    assert all("do not simulate" in facts(row)["conditions"] for row in rows)


def saved_raccoon(save_factory, *, day=10, season=2, delivered=(False, False), last=0):
    state = save_factory()
    text = state.source.read_text().replace(
        "<dayOfMonth>1</dayOfMonth>", f"<dayOfMonth>{day}</dayOfMonth>"
    )
    text = text.replace("<daysPlayed>1</daysPlayed>", f"<daysPlayed>{day}</daysPlayed>")
    bundle = "".join(f"<boolean>{str(done).lower()}</boolean>" for done in delivered)
    text = text.replace(
        "</SaveGame>",
        f"<timesFedRaccoons>1</timesFedRaccoons><seasonOfCurrentRaccoonBundle>{season}</seasonOfCurrentRaccoonBundle><raccoonBundles>{bundle}</raccoonBundles><daysPlayedWhenLastRaccoonBundleWasFinished>{last}</daysPlayedWhenLastRaccoonBundleWasFinished></SaveGame>",
    )
    state.source.write_text(text)
    return load_save(state.source)


def test_current_raccoon_uses_locked_season_and_skips_delivered_ingredients(
    save_factory, data
):
    state = saved_raccoon(save_factory, season=2)
    first = next(
        row for row in records(state, data, "raccoon", 2) if facts(row)["slot"] == 1
    )
    assert first.item_name == "Dried Blackberry"
    assert first.alternatives == ()
    assert facts(first)["request_state"] == "active"
    state = saved_raccoon(save_factory, season=2, delivered=(True, False))
    rows = records(state, data, "raccoon", 2)
    assert [facts(row)["slot"] for row in rows] == [2, 3]


@pytest.mark.parametrize(
    "day,last,season,item", [(21, 13, 0, "Dried Cherry"), (22, 14, 1, "Dried Peach")]
)
def test_raccoon_activation_rolls_to_next_season_after_day_21(
    save_factory, data, day, last, season, item
):
    state = saved_raccoon(save_factory, day=day, season=-1, last=last)
    first = records(state, data, "raccoon", 2)[0]
    assert first.item_name == item
    assert facts(first)["request_season"] == season
    assert facts(first)["request_state"] == "ready_to_activate"


def test_raccoon_cooldown_and_future_requests_remain_conditional(save_factory, data):
    state = saved_raccoon(save_factory, day=20, season=-1, last=15)
    rows = records(state, data, "raccoon", 2, 2)
    current = next(row for row in rows if row.sequence == 2 and facts(row)["slot"] == 1)
    future = next(row for row in rows if row.sequence == 3 and facts(row)["slot"] == 1)
    assert current.item_name is None and len(current.alternatives) == 4
    assert facts(current)["request_state"] == "cooldown"
    assert facts(current)["available_after_day"] == 23
    assert future.item_name is None and len(future.alternatives) == 4
    assert facts(future)["request_state"] == "future"


def mystery_seed_state(save_factory):
    state = save_factory(player_id=-2062291679424207820)
    state.source.write_text(
        state.source.read_text().replace(
            "<mailReceived>", "<mailReceived><string>GotMysteryBook</string>"
        )
    )
    return load_save(state.source)


@pytest.mark.parametrize(
    "day,expected",
    [
        (1, {"472", "473", "474", "475"}),
        (29, {"487", "483", "482", "484"}),
        (57, {"487", "488", "489", "490"}),
        (
            85,
            {
                "472",
                "473",
                "474",
                "475",
                "487",
                "483",
                "482",
                "484",
                "488",
                "489",
                "490",
            },
        ),
    ],
)
def test_mystery_seasonal_seed_candidates_use_unsaved_session_rng(
    save_factory, data, day, expected
):
    state = mystery_seed_state(save_factory)
    state = replace(state, metadata=replace(state.metadata, days_played=day))
    row = container(
        records(state, data, "mystery", 97), "Golden Mystery Box with Farming Mastery"
    )
    assert row.item_id is None and row.quantity == 20
    assert facts(row)["certainty"] == "session_dependent"
    assert {alt.item_id for alt in row.alternatives} == {
        "(O)" + item_id for item_id in expected
    }
    assert all(
        alt.quantity == 20 and "Session RNG" in alt.condition
        for alt in row.alternatives
    )


@pytest.mark.parametrize(
    "day,item_id",
    [
        (23, "CarrotSeeds"),
        (24, "SummerSquashSeeds"),
        (48, "SummerSquashSeeds"),
        (49, "BroccoliSeeds"),
        (76, "BroccoliSeeds"),
        (77, "PowdermelonSeeds"),
        (104, "PowdermelonSeeds"),
        (105, "CarrotSeeds"),
    ],
)
def test_dated_raccoon_seeds_match_game_thresholds_for_boxes_and_prizes(
    save_factory, data, day, item_id
):
    state = mystery_seed_state(save_factory)
    state = replace(state, metadata=replace(state.metadata, days_played=day))
    mystery = container(
        records(state, data, "mystery", 101), "Golden Mystery Box with Farming Mastery"
    )
    prize = records(state, data, "prize", 1)[0]
    assert (mystery.item_id, mystery.quantity) == ("(O)" + item_id, 8)
    assert (prize.item_id, prize.quantity) == ("(O)" + item_id, 12)
    assert "saved date" in facts(mystery)["opening_rule"]
    assert "saved date" in facts(prize)["conditions"]


def test_unknown_claim_date_exposes_four_seed_options(save_factory, data):
    state = save_factory()
    state = replace(state, metadata=replace(state.metadata, days_played=None))
    prize = records(state, data, "prize", 1)[0]
    assert prize.item_id is None and len(prize.alternatives) == 4
    reward = next(
        row
        for row in records(state, data, "raccoon", 1)
        if facts(row)["role"] == "reward"
    )
    assert reward.item_id is None and len(reward.alternatives) == 4
    assert all("Date obtained:" in alt.condition for alt in reward.alternatives)
    assert all(alt.quantity == 25 for alt in reward.alternatives)


@pytest.mark.parametrize(
    "sequence,item_id",
    [(11, "(H)SportsCap"), (14, "(F)FancyHousePlant1"), (26, "(F)FancyTree3")],
)
def test_prize_hats_and_plants_keep_the_qualified_game_id(
    save_factory, data, sequence, item_id
):
    state = save_factory(player_id=-2062291679424207820)
    assert records(state, data, "prize", sequence)[0].item_id == item_id


def test_raccoon_hat_keeps_its_qualified_game_id(save_factory, data):
    reward = next(
        row
        for row in records(save_factory(), data, "raccoon", 3)
        if facts(row)["role"] == "reward"
    )
    assert reward.item_id == "(H)RaccoonHat"


TOOL_SERIALIZATION_REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures/game-tool-serialization.json").read_text()
)


@pytest.mark.parametrize(
    "case",
    TOOL_SERIALIZATION_REFERENCE["cases"],
    ids=lambda case: (
        "repeated-elements" if case["populated"] else "omitted-empty-lists"
    ),
)
def test_original_tool_xml_roundtrip_preserves_enchantment_state(
    save_factory, data, case
):
    state = save_factory(
        game_id=ENCHANTMENT_REFERENCE["game_id"],
        player_id=ENCHANTMENT_REFERENCE["player_id"],
    )
    xml = case["xml"].split("?>", 1)[1]
    state.source.write_text(
        state.source.read_text().replace("</player>", f"<items>{xml}</items></player>")
    )
    state = load_save(state.source)
    item = state.player.inventory[0]
    assert item.enchantments == (
        frozenset({"GenerousEnchantment"}) if case["populated"] else frozenset()
    )
    row = next(
        row
        for row in records(state, data, "enchant", 1)
        if facts(row).get("tool_slot") == 1
    )
    aliases = {"Expansive": "Reaching"}
    assert facts(row)["previous_enchantments"] == tuple(
        aliases.get(name, name) for name in case["previous"]
    )
    assert facts(row)["eligible_enchantments"] == tuple(
        aliases.get(name, name) for name in case["pool"]
    )
    assert row.item_name == aliases.get(case["selected"], case["selected"])
    assert facts(row)["certainty"] == "saved_tool_state"
