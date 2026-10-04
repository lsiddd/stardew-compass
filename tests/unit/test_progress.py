"""Native progress regression facts, including all legacy sections and version branches."""

from dataclasses import FrozenInstanceError
import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from lxml import etree
from stardew.domain.progress import PROGRESS_SECTIONS, analyze_progress
from stardew.domain.progress.common import Context
from stardew.infrastructure.game_data.loader import load_game_data
from stardew.infrastructure.saves.loader import from_snapshot, snapshot


def dictionary(name, records, *, kind="int"):
    return (
        "<"
        + name
        + ">"
        + "".join(
            f"<item><key><string>{key}</string></key><value><{kind}>{val}</{kind}></value></item>"
            for key, val in records.items()
        )
        + "</"
        + name
        + ">"
    )


def player_xml(name="Farmer", player_id="999999999999999999", *, recipes=1):
    stats = {
        "daysPlayed": 120,
        "questsCompleted": 40,
        "MasteryExp": 25000,
        "mastery_0": 0,
        "monstersKilled": 1000,
        "Book_AnimalCatalogue": 1,
    }
    return f"""<name>{name}</name><farmName>Fixture</farmName><UniqueMultiplayerID>{player_id}</UniqueMultiplayerID>
    <totalMoneyEarned>50000</totalMoneyEarned><maxStamina>508</maxStamina><houseUpgradeLevel>3</houseUpgradeLevel><spouse>Abigail</spouse>
    <farmingLevel>10</farmingLevel><fishingLevel>10</fishingLevel><foragingLevel>10</foragingLevel><miningLevel>10</miningLevel><combatLevel>10</combatLevel><luckLevel>0</luckLevel><isMale>true</isMale>
    <deepestMineLevel>60</deepestMineLevel><hasSkullKey>true</hasSkullKey><hasRustyKey>true</hasRustyKey>
    <experiencePoints><int>15000</int><int>15000</int><int>15000</int><int>100</int><int>0</int></experiencePoints>
    <stats>{"".join(f"<{key}>{val}</{key}>" for key, val in stats.items())}{dictionary("Values", stats)}{dictionary("specificMonstersKilled", {"Fly": 80, "Green Slime": 20})}</stats>
    <mailReceived><string>CF_Fair</string><string>CF_Spouse</string><string>gotMaxStamina</string><string>HasSkullKey</string><string>HasRustyKey</string><string>Island_FirstParrot</string><string>gotPearl</string><string>canReadJunimoText</string><string>Beat_PK</string><string>raccoonMovedIn</string></mailReceived>
    <eventsSeen><int>1</int><int>2120303</int></eventsSeen>
    <friendshipData><item><key><string>Abigail</string></key><value><Friendship><Points>3500</Points><Status>Married</Status></Friendship></value></item></friendshipData>
    <friendships><item><key><string>Abigail</string></key><value><ArrayOfInt><int>3500</int></ArrayOfInt></value></item></friendships>
    {dictionary("cookingRecipes", {"Fried Egg": 0})}{dictionary("recipesCooked", {"194": 2})}
    {dictionary("craftingRecipes", {"Gate": 1, "Wedding Ring": 1, "Custom Item": 1})}{dictionary("basicShipped", {"24": 300, "188": 15})}
    <fishCaught><item><key><string>(O)128</string></key><value><ArrayOfInt><int>100</int><int>10</int></ArrayOfInt></value></item><item><key><string>372</string></key><value><ArrayOfInt><int>1</int></ArrayOfInt></value></item><item><key><string>898</string></key><value><ArrayOfInt><int>1</int></ArrayOfInt></value></item></fishCaught>
    <archaeologyFound><item><key><int>96</int></key><value><ArrayOfInt><int>1</int></ArrayOfInt></value></item><item><key><int>97</int></key><value><ArrayOfInt><int>0</int></ArrayOfInt></value></item></archaeologyFound>
    {dictionary("mineralsFound", {"60": 3})}<secretNotesSeen><int>13</int><int>27</int><int>1001</int></secretNotesSeen>
    <chestConsumedLevels><item><key><int>100</int></key><value><boolean>true</boolean></value></item></chestConsumedLevels>
    <JOTPKProgress><whichRound><int>1</int></whichRound><whichWave><int>2</int></whichWave><died><boolean>false</boolean></died></JOTPKProgress>
    <achievements><int>5</int><int>26</int></achievements>"""


def make_state(game_version="1.6.15", extra_player=""):
    xml = f"""<SaveGame xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><gameVersion>{game_version}</gameVersion><whichFarm>0</whichFarm><dayOfMonth>7</dayOfMonth><currentSeason>spring</currentSeason><year>2</year><uniqueIDForThisGame>345</uniqueIDForThisGame><player>{player_xml()}</player><farmhands>{extra_player}</farmhands>
    <locations><GameLocation xsi:type="Farm"><name>Farm</name><grandpaScore>2</grandpaScore><buildings><Building><buildingType>Earth Obelisk</buildingType></Building><Building><buildingType>Coop</buildingType><currentOccupants>1</currentOccupants><maxOccupants>4</maxOccupants><indoors><Animals><SerializableDictionaryOfInt64FarmAnimal><item><value><FarmAnimal><name>Hen</name><myID>1234</myID><type>White Chicken</type><hasEatenAnimalCracker>true</hasEatenAnimalCracker></FarmAnimal></value></item></SerializableDictionaryOfInt64FarmAnimal></Animals></indoors></Building></buildings><characters><NPC><name>Abigail</name><datable>true</datable><gender>1</gender></NPC><NPC xsi:type="Pet"><name>Cat</name><petType>Cat</petType><friendshipTowardFarmer>1000</friendshipTowardFarmer></NPC></characters></GameLocation>
    <GameLocation xsi:type="FarmHouse"><characters><NPC xsi:type="Child"><name>Alice</name></NPC><NPC xsi:type="Child"><name>Bob</name></NPC></characters></GameLocation>
    <GameLocation xsi:type="LibraryMuseum"><museumPieces><item><key><Vector2><X>1</X><Y>1</Y></Vector2></key><value><int>60</int></value></item><item><key><Vector2><X>2</X><Y>2</Y></Vector2></key><value><int>96</int></value></item></museumPieces></GameLocation>
    <GameLocation xsi:type="CommunityCenter"><areasComplete><boolean>false</boolean><boolean>false</boolean><boolean>false</boolean><boolean>false</boolean><boolean>false</boolean><boolean>false</boolean></areasComplete><bundles><item><key><int>0</int></key><value><ArrayOfBoolean><boolean>true</boolean><boolean>false</boolean><boolean>false</boolean><boolean>false</boolean></ArrayOfBoolean></value></item></bundles></GameLocation></locations>
    {dictionary("bundleData", {"Pantry/0": "Spring Crops/O 465 20/24 1 0 188 1 0 190 1 0 192 1 0/0///Spring Crops"}, kind="string")}
    <completedSpecialOrders><string>Caroline</string><string>QiChallenge2</string></completedSpecialOrders>
    <collectedNutTracker><string>Bush_IslandEast_17_37</string><string>Mermaid</string></collectedNutTracker>{dictionary("limitedNutDrops", {"Birdie": 99})}
    <goldenCoconutCracked>true</goldenCoconutCracked><goldenWalnutsFound>12</goldenWalnutsFound><perfectionWaivers>2</perfectionWaivers><timesFedRaccoons>9</timesFedRaccoons><daysPlayedWhenLastRaccoonBundleWasFinished>100</daysPlayedWhenLastRaccoonBundleWasFinished>
    <junimoKartLeaderboards><entries><NetLeaderboardsEntry><name><string>Farmer</string></name><score><int>40000</int></score></NetLeaderboardsEntry></entries></junimoKartLeaderboards></SaveGame>"""
    return from_snapshot(snapshot(etree.fromstring(xml.encode())), Path("fixture"))


def test_summary_does_not_run_unrelated_progress_rules(data, monkeypatch):
    from stardew.domain.progress import RULES

    def unavailable_rule(context):
        raise RuntimeError("unrelated calculation must not run")

    state = make_state()
    expected = analyze_progress(state, data, ("summary",))
    for section in RULES:
        if section != "summary":
            monkeypatch.setitem(RULES, section, unavailable_rule)
    assert analyze_progress(state, data, ("summary",)) == expected
    assert analyze_progress(state, data, ()) == ()


def test_money_uses_exact_saved_integer(data):
    value = 9007199254740993
    xml = f"""<SaveGame><uniqueIDForThisGame>42</uniqueIDForThisGame>
      <player><name>Farmer</name><totalMoneyEarned>{value}</totalMoneyEarned></player>
      </SaveGame>"""
    state = from_snapshot(snapshot(etree.fromstring(xml.encode())), Path("fixture"))
    result = analyze_progress(state, data, ("money",))[0]
    assert (
        dict((fact.name, fact.value) for fact in result.facts)["total_money_earned"]
        == value
    )


@pytest.fixture(scope="module")
def data():
    return load_game_data()


@pytest.fixture(scope="module")
def results(data):
    return {
        result.section_id: result for result in analyze_progress(make_state(), data)
    }


def get_metric(result, key):
    return next(
        m
        for m in result.metrics + (result.players[0].metrics if result.players else ())
        if m.metric_id == key
    )


# Reference facts independently read from the pinned rules, one for every exposed section.
REFERENCE = json.loads(
    (Path(__file__).parents[1] / "fixtures" / "progress_reference_v2.json").read_text()
)


@pytest.mark.parametrize(
    "section,key,count,goal",
    [
        (case["section_id"], case["metric_id"], case["count"], case["goal"])
        for case in REFERENCE["metric_cases"]
    ],
)
def test_all_section_reference_counts(results, section, key, count, goal):
    found = get_metric(results[section], key)
    assert (found.count, found.goal) == (count, goal)


def test_summary_and_animal_reference_facts(results):
    assert len(results) == 27
    assert tuple(results) == PROGRESS_SECTIONS
    summary = {fact.name: fact.value for fact in results["summary"].facts}
    assert {
        key: summary[key] for key in REFERENCE["section_facts"]["summary"]
    } == REFERENCE["section_facts"]["summary"]
    animals = results["animals"].items
    assert [
        {"name": item.name, "count": item.count, "category": item.category}
        for item in animals
    ] == REFERENCE["section_facts"]["animals"]["items"]


def test_mod_recipes_wedding_ring_and_distinct_fish(results):
    crafted = results["crafting"].players[0]
    assert {f.name: f.value for f in crafted.facts} == {
        "known_recipes": 1,
        "mod_known": 1,
        "mod_crafted": 1,
    }
    assert get_metric(results["crafting"], "diy").count == 2
    fishing = {f.name: f.value for f in results["fishing"].players[0].facts}
    assert fishing["total_catches"] == 102
    assert fishing["unique_catches"] == 3
    assert get_metric(results["fishing"], "bobber_styles").count == 2


@pytest.mark.parametrize(
    "game_version,expected",
    [("1.2", 71), ("1.3", 71), ("1.4", 74), ("1.5", 80), ("1.6.15", 81)],
)
def test_recipe_version_branches(data, game_version, expected):
    result = analyze_progress(
        make_state(game_version),
        data,
        ("cooking", "fishing", "monsters", "skill_mastery"),
    )
    assert get_metric(result[0], "cooking").goal == expected
    assert get_metric(result[1], "fishing").count == (1 if game_version < "1.6" else 2)
    assert get_metric(result[2], "protector_of_the_valley").goal == (
        7 if game_version < "1.4" else 11 if game_version < "1.5" else 12
    )
    assert result[3].available == (game_version >= "1.6")


def test_perfection_selection_order_and_call_isolation(data):
    state = make_state()
    full = analyze_progress(state, data)
    selected = analyze_progress(state, data, ("perfection_tracker", "money", "social"))
    assert selected[0] == next(r for r in full if r.section_id == "perfection_tracker")
    assert full == analyze_progress(state, data)
    with pytest.raises(FrozenInstanceError):
        selected[0].title = "changed"
    assert state.snapshot.value("player/name") == "Farmer"


def test_perfection_uses_best_player_per_category(data):
    host = make_state()
    farmhand = (
        "<Farmer>"
        + player_xml("Farmhand", "-9223372036854775808")
        .replace("<string>Gate</string>", "<string>Bomb</string>")
        .replace("<string>24</string>", "<string>190</string>")
        .replace("<string>188</string>", "<string>192</string>")
        + "</Farmer>"
    )
    state = make_state(extra_player=farmhand)
    ctx = Context(state, data)
    from stardew.domain.progress.completion import perfection

    first, second = (ctx.player_id(p) for p in state.players)
    ctx.perfection[first] = {"cooking": (81, 81), "shipping": (1, 155)}
    ctx.perfection[second] = {"cooking": (1, 81), "shipping": (155, 155)}
    result = perfection(ctx)
    assert get_metric(result, "cooking").player_id == first
    assert get_metric(result, "shipping").player_id == second
    assert get_metric(result, "cooking").earned == 10
    assert get_metric(result, "shipping").earned == 15


def test_stamina_override_and_walnut_tracking(results):
    assert get_metric(results["stardrops"], "stardrops").count == 3
    assert get_metric(results["perfection_tracker"], "stardrops").count == 1
    walnut = {fact.name: fact.value for fact in results["walnuts"].facts}
    assert (
        walnut["tracked_walnuts"] == 12
    )  # 1 bush + 5 mermaid + capped 5 Birdie + coconut.
    assert not results["walnuts"].diagnostics


def test_invalid_section_is_explicit_error(data):
    with pytest.raises(ValueError, match="unknown_section"):
        analyze_progress(make_state(), data, ("unknown_section",))


def test_missing_player_ids_keep_individual_statistics(data):
    xml = (
        "<Farmer>"
        + player_xml("Farmhand A", "")
        + "</Farmer><Farmer>"
        + player_xml("Farmhand B", "")
        .replace("<daysPlayed>120</daysPlayed>", "<daysPlayed>99</daysPlayed>")
        .replace("<int>120</int>", "<int>99</int>")
        + "</Farmer>"
    )
    state = make_state(extra_player=xml)
    assert len(state.players) == 3
    ctx = Context(state, data)
    keys = tuple(ctx.player_id(player) for player in state.players)
    assert keys == ("999999999999999999", "player_1", "player_2")
    assert len(ctx.stats) == 3
    assert ctx.stats["player_1"]["daysPlayed"] == 120
    assert ctx.stats["player_2"]["daysPlayed"] == 99
    assert ctx.host_id == "999999999999999999"


def test_zero_perfection_keeps_category_goals(data):
    from stardew.domain.progress.completion import perfection

    ctx = Context(make_state(), data)
    key = ctx.host_id
    ctx.perfection[key] = {"cooking": (0, 81), "crafting": (0, 149)}
    result = perfection(ctx)
    assert get_metric(result, "cooking").goal == 81
    assert get_metric(result, "crafting").goal == 149
    assert get_metric(result, "cooking").player_id == key


def test_structured_skill_relationship_and_cost_details(results):
    mining = next(
        item for item in results["skills"].players[0].items if item.item_id == "mining"
    )
    assert (mining.count, mining.level, mining.next_goal, mining.next_missing) == (
        100,
        1,
        380,
        280,
    )
    relationship = next(
        item for item in results["social"].players[0].items if item.item_id == "Abigail"
    )
    assert (
        relationship.count,
        relationship.goal,
        relationship.status,
        relationship.hearts,
    ) == (3500, 3500, "Married", 14)
    event = next(
        item for item in results["social"].players[0].items if item.item_id == "1"
    )
    assert (event.event_ids, event.hearts, event.status) == (("1",), 2, "seen")
    upgrade = next(
        item
        for item in results["island_upgrades"].items
        if item.item_id == "Island_Turtle"
    )
    assert (upgrade.cost, upgrade.cost_unit) == (10, "walnuts")
    bundle = next(item for item in results["bundles"].items if item.item_id == "188")
    assert (bundle.goal, bundle.quality) == (1, 0)


def test_default_secret_note_statue_does_not_count_as_collected(data):
    from dataclasses import replace
    from stardew.domain.models import SaveNode, freeze
    from stardew.domain.progress import world

    def build(tag, text=None, children=()):
        return SaveNode(tag, text, freeze({}), tuple(children))

    statue = build("Object", children=(build("name", "Stone Junimo"),))
    position = build("Vector2", children=(build("X", "57"), build("Y", "16")))
    entry = build(
        "item",
        children=(
            build("key", children=(position,)),
            build("value", children=(statue,)),
        ),
    )
    town = build(
        "GameLocation",
        children=(build("name", "Town"), build("objects", children=(entry,))),
    )
    state = make_state()
    old_locations = state.snapshot.find("locations")
    locations = replace(old_locations, children=old_locations.children + (town,))
    root = replace(
        state.snapshot,
        children=tuple(
            locations if node is old_locations else node
            for node in state.snapshot.children
        ),
    )
    state = replace(state, snapshot=root)
    result = world.notes(Context(state, data))
    assert get_metric(result, "note_rewards").count == 2
    assert any(
        item.item_id == "14" and item.category == "note_reward"
        for item in result.players[0].items
    )


def test_case_specific_monster_identity_is_preserved(data):
    state = make_state()
    ctx = Context(state, data)
    from dataclasses import replace
    from stardew.domain.models import SaveNode
    from stardew.domain.progress.player import monsters

    node = state.players[0].snapshot
    kills = node.find("stats/specificMonstersKilled")
    fly = next(item for item in kills.children if item.value("key/string") == "Fly")
    renamed = replace(fly.find("key/string"), content="Cave Fly")
    key = replace(fly.find("key"), children=(renamed,))
    fly = replace(fly, children=(key, fly.find("value")))
    kills = replace(kills, children=(fly,) + kills.children[1:])
    stats = replace(
        node.find("stats"),
        children=tuple(
            kills if item.tag == "specificMonstersKilled" else item
            for item in node.find("stats").children
        ),
    )
    node = replace(
        node,
        children=tuple(
            stats if item.tag == "stats" else item for item in node.children
        ),
    )
    farmer = replace(state.players[0], snapshot=node)
    ctx.players = (farmer,)
    result = monsters(ctx)
    assert get_metric(result, "protector_of_the_valley").count == 0


def test_host_and_farmhand_have_distinct_upgrade_goals(data):
    farmhand = (
        "<Farmer>"
        + player_xml("Farmhand", "2").replace(
            "<houseUpgradeLevel>3</houseUpgradeLevel>",
            "<houseUpgradeLevel>2</houseUpgradeLevel>",
        )
        + "</Farmer>"
    )
    result = analyze_progress(make_state(extra_player=farmhand), data, ("family",))[0]
    host, guest = result.players
    host_metric = next(
        metric for metric in host.metrics if metric.metric_id == "house_fully_upgraded"
    )
    guest_metric = next(
        metric for metric in guest.metrics if metric.metric_id == "house_fully_upgraded"
    )
    assert (host_metric.count, host_metric.goal, host_metric.complete) == (3, 3, True)
    assert (guest_metric.count, guest_metric.goal, guest_metric.complete) == (
        2,
        2,
        True,
    )


def test_zero_friendships_contribute_zero_to_perfection(data):
    from dataclasses import replace

    node = make_state().snapshot
    farmer = node.find("player")
    friendship = farmer.find("friendshipData")
    farmer = replace(
        farmer,
        children=tuple(
            replace(friendship, children=()) if child is friendship else child
            for child in farmer.children
        ),
    )
    node = replace(
        node,
        children=tuple(
            farmer if child.tag == "player" else child for child in node.children
        ),
    )
    state = from_snapshot(node, Path("zero-friendships"))
    result = analyze_progress(state, data, ("social", "perfection_tracker"))
    friendship_metric = get_metric(result[0], "great_friends")
    perfection_metric = get_metric(result[1], "great_friends")
    assert (
        friendship_metric.count,
        friendship_metric.goal,
        friendship_metric.percentage,
        friendship_metric.complete,
    ) == (0, 0, 0, False)
    assert (
        perfection_metric.count,
        perfection_metric.goal,
        perfection_metric.earned,
    ) == (0, 0, 0)
    assert any(
        "no tracked targets" in diagnostic for diagnostic in result[1].diagnostics
    )


def test_stamina_override_changes_perfection_without_changing_marker_facts(data):
    from dataclasses import replace

    state = make_state()
    yes = analyze_progress(state, data, ("stardrops", "perfection_tracker"))
    farmer = state.snapshot.find("player")
    mail = farmer.find("mailReceived")
    mail = replace(
        mail,
        children=tuple(
            flag for flag in mail.children if flag.content != "gotMaxStamina"
        ),
    )
    farmer = replace(
        farmer,
        children=tuple(
            mail if child.tag == "mailReceived" else child for child in farmer.children
        ),
    )
    root = replace(
        state.snapshot,
        children=tuple(
            farmer if child.tag == "player" else child
            for child in state.snapshot.children
        ),
    )
    state = from_snapshot(root, Path("without-stamina-override"))
    no = analyze_progress(state, data, ("stardrops", "perfection_tracker"))
    assert (
        get_metric(yes[0], "stardrops").count
        == get_metric(no[0], "stardrops").count
        == 3
    )
    assert get_metric(yes[1], "stardrops").earned == 10
    assert get_metric(no[1], "stardrops").earned == 0


def test_progress_uses_exact_loaded_player_statistics(data):
    from dataclasses import replace

    root = make_state().snapshot
    farmer = root.find("player")
    stats = farmer.find("stats")
    entries = stats.find("Values")
    day_entry = next(
        item for item in entries.children if item.value("key/string") == "daysPlayed"
    )
    large = 9007199254740993
    day_value = replace(day_entry.find("value/int"), content=str(large))
    day_entry = replace(
        day_entry,
        children=(
            day_entry.find("key"),
            replace(day_entry.find("value"), children=(day_value,)),
        ),
    )
    entries = replace(
        entries,
        children=tuple(
            day_entry if item.value("key/string") == "daysPlayed" else item
            for item in entries.children
        ),
    )
    stats = replace(
        stats,
        children=tuple(
            entries if child.tag == "Values" else child for child in stats.children
        ),
    )
    farmer = replace(
        farmer,
        children=tuple(
            stats if child.tag == "stats" else child for child in farmer.children
        ),
    )
    root = replace(
        root,
        children=tuple(
            farmer if child.tag == "player" else child for child in root.children
        ),
    )
    state = from_snapshot(root, Path("large-day-count"))
    result = analyze_progress(state, data, ("summary", "raccoons"))
    summary = {fact.name: fact.value for fact in result[0].facts}
    raccoons = {fact.name: fact.value for fact in result[1].facts}
    assert (
        state.metadata.days_played
        == state.players[0].stats["daysPlayed"]
        == summary["days_played"]
        == large
    )
    assert raccoons["days_since_fed"] == large - 100


def test_text_and_json_preserve_progress_details(data):
    from stardew.api import analyze, AnalysisOptions
    from stardew.presentation.json import render_json
    from stardew.presentation.text import render_text

    result = analyze(
        make_state(),
        data=data,
        options=AnalysisOptions(
            progress=("skills", "social", "bundles", "island_upgrades"),
            predictions=(),
            extras=False,
            bubbles=False,
            artifacts=False,
        ),
    )
    original = render_json(result)
    payload = json.loads(original)
    selected = {section["section_id"]: section for section in payload["progress"]}
    mining = next(
        item
        for item in selected["skills"]["players"][0]["items"]
        if item["item_id"] == "mining"
    )
    assert {
        key: mining[key]
        for key in ("count", "goal", "level", "next_goal", "next_missing")
    } == {
        "count": 100,
        "goal": 15000,
        "level": 1,
        "next_goal": 380,
        "next_missing": 280,
    }
    relationship = next(
        item
        for item in selected["social"]["players"][0]["items"]
        if item["item_id"] == "Abigail"
    )
    assert (
        relationship["count"],
        relationship["goal"],
        relationship["hearts"],
        relationship["status"],
    ) == (3500, 3500, 14, "Married")
    event = next(
        item
        for item in selected["social"]["players"][0]["items"]
        if item["item_id"] == "1"
    )
    assert event["event_ids"] == ["1"] and event["status"] == "seen"
    bundle = next(
        item for item in selected["bundles"]["items"] if item["item_id"] == "188"
    )
    assert (bundle["goal"], bundle["missing"], bundle["quality"]) == (1, 1, 0)
    turtle = next(
        item
        for item in selected["island_upgrades"]["items"]
        if item["item_id"] == "Island_Turtle"
    )
    assert (turtle["cost"], turtle["cost_unit"]) == (10, "walnuts")
    text = render_text(result, data=data)
    for detail in (
        "level: 1",
        "next goal: 380",
        "next missing: 280",
        "3500/3500",
        "hearts: 14",
        "status: Married",
        "event ids: 1",
        "quality: 0",
        "cost: 10",
        "cost unit: walnuts",
    ):
        assert detail in text
    assert render_json(result) == original
    assert "snapshot" not in payload
