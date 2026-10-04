from dataclasses import asdict, replace
import json
from pathlib import Path
import pytest
from stardew.domain.numeric import Random
from types import SimpleNamespace
from stardew.domain.predictions.artifacts import ArtifactState, ArtifactSpot
from stardew.domain.predictions.artifacts import ArtifactPredictor, condition

FIXTURES = Path(__file__).parents[1] / "fixtures"


@pytest.fixture(scope="module")
def artifact_predictor(tmp_path_factory):
    from stardew.domain.models.state import freeze

    return ArtifactPredictor(
        freeze(
            {
                name: json.loads(
                    (FIXTURES / ("artifact-" + name + ".json")).read_text()
                )
                for name in ("Objects", "Locations", "ObjectNames")
            }
        )
    )


SAVE_FIELDS = {
    "Seed": "game_id",
    "DaysPlayed": "days_played",
    "Season": "season",
    "Day": "day",
    "Year": "year",
    "Version": "game_version",
    "LegacyRandom": "use_legacy_random",
    "TimesFished": "times_fished",
    "FarmType": "farm_type",
}
STATE_FIELDS = {
    "Save": "save",
    "Spots": "spots",
    "Mail": "mail",
    "Orders": "orders",
    "OrderRules": "order_rules",
    "Dug": "dug",
    "Totems": "totems",
    "LostBooks": "lost_books",
    "DailyLuck": "daily_luck",
    "LuckLevel": "luck_level",
    "MiningLevel": "mining_level",
    "FarmingMastery": "farming_mastery",
    "GoldenCoconutCracked": "golden_coconut_cracked",
    "BridgeFixed": "bridge_fixed",
    "Generous": "generous",
    "Archaeologist": "archaeologist",
}
SPOT_FIELDS = {"Location": "location", "X": "x", "Y": "y"}
ITEM_FIELDS = {
    "Id": "item_id",
    "Name": "name",
    "Quantity": "quantity",
    "RuntimeDependent": "runtime_dependent",
}

# Keep the captured C# fixtures intact; only generated presentation labels change.
REFERENCE_LABELS = {
    "Mapa de festival salvo, indisponível fora do festival.": "Saved festival map; available only during the festival.",
    "Bilhete ou pedra: depende do RNG da sessão, não salvo no arquivo.": "Note or stone depends on session RNG, which is not stored in the save.",
    "Bilhete secreto OU pedra (RNG da sessão)": "Secret note OR stone (session RNG)",
}


def state_from_json(data):
    data = {STATE_FIELDS[k]: v for k, v in data.items()}
    data["save"] = SimpleNamespace(
        **{SAVE_FIELDS[k]: v for k, v in data["save"].items()}
    )
    data["spots"] = tuple(
        ArtifactSpot(**{SPOT_FIELDS[k]: v for k, v in s.items()}) for s in data["spots"]
    )
    for key in ("mail", "orders", "order_rules"):
        data[key] = frozenset(data[key])
    return ArtifactState(**data)


def expected_result(case):
    result = case["result"]
    items = []
    for item in result["Items"]:
        converted = {ITEM_FIELDS[k]: v for k, v in item.items()}
        converted["name"] = REFERENCE_LABELS.get(converted["name"], converted["name"])
        converted["alternatives"] = (
            (
                ("(O)842", "(O)390")
                if result["Location"].startswith("Island")
                else ("(O)79", "(O)390")
            )
            if item["RuntimeDependent"]
            else ()
        )
        items.append(converted)
    return {
        "location": result["Location"],
        "x": result["X"],
        "y": result["Y"],
        "items": tuple(items),
        "note": REFERENCE_LABELS.get(result["Note"], result["Note"]),
    }


@pytest.mark.parametrize(
    "case",
    json.loads((FIXTURES / "artifacts.json").read_text()),
    ids=lambda c: str(c["spot"]["X"]),
)
def test_csharp_artifacts(case, artifact_predictor):
    state, spot = (
        state_from_json(case["state"]),
        ArtifactSpot(**{SPOT_FIELDS[k]: v for k, v in case["spot"].items()}),
    )
    assert asdict(artifact_predictor.predict(state, spot)) == expected_result(case)


def test_conditions_and_short_circuit(artifact_predictor):
    state = ArtifactState(
        SimpleNamespace(
            game_id=1,
            days_played=1,
            season="winter",
            day=1,
            year=1,
            game_version="1.6.15",
            use_legacy_random=False,
            times_fished=0,
            farm_type=0,
        ),
        (),
        frozenset({"flag"}),
        frozenset({"order"}),
        frozenset({"rule"}),
        bridge_fixed=True,
        luck_level=2,
        mining_level=3,
    )
    spot = ArtifactSpot("IslandNorth", 4, 8)
    r = Random(0)
    assert condition(
        "PLAYER_HAS_MAIL Target flag, PLAYER_SPECIAL_ORDER_ACTIVE Target order, "
        "PLAYER_SPECIAL_ORDER_RULE_ACTIVE Target rule, IS_ISLAND_NORTH_BRIDGE_FIXED, "
        "LOCATION_SEASON Here SUMMER, PLAYER_LUCK_LEVEL Target 2, PLAYER_MINING_LEVEL Target 3",
        state,
        spot,
        r,
    )
    assert not condition("DAYS_PLAYED 2, UNSUPPORTED", state, spot, r)
    with pytest.raises(ValueError, match="Unsupported condition"):
        condition("UNSUPPORTED", state, spot, r)
    assert (
        artifact_predictor.resolve("LOST_BOOK_OR_ITEM (O)770", state, spot, r)
        == "(O)102"
    )
    assert (
        artifact_predictor.resolve(
            "LOST_BOOK_OR_ITEM (O)770", replace(state, lost_books=21), spot, r
        )
        == "(O)770"
    )
    assert (
        artifact_predictor.resolve(
            "SECRET_NOTE_OR_ITEM (O)390", state, ArtifactSpot("Town", 0, 0), r
        )
        == "(O)390"
    )
    assert artifact_predictor.resolve(
        "SECRET_NOTE_OR_ITEM (O)390", state, spot, r
    ).startswith("runtime:")


@pytest.mark.parametrize("index", [0, 1])
def test_artifact_rules_use_shared_loaded_state(
    index, tmp_path, artifact_predictor, monkeypatch
):
    """Native model extraction must preserve rule inputs and reuse the one read."""
    import xml.etree.ElementTree as ET
    from stardew.infrastructure.saves.loader import load_save

    case = json.loads((FIXTURES / "artifacts.json").read_text())[index]
    baseline, metadata = case["state"], case["state"]["Save"]
    root = ET.Element("SaveGame")

    def field(node, tag, value):
        ET.SubElement(node, tag).text = (
            str(value).lower() if isinstance(value, bool) else str(value)
        )

    for tag, key in (
        ("uniqueIDForThisGame", "Seed"),
        ("currentSeason", "Season"),
        ("dayOfMonth", "Day"),
        ("year", "Year"),
        ("gameVersion", "Version"),
        ("useLegacyRandom", "LegacyRandom"),
        ("whichFarm", "FarmType"),
    ):
        field(root, tag, metadata[key])
    for tag, key in (
        ("treasureTotemsUsed", "Totems"),
        ("lostBooksFound", "LostBooks"),
        ("dailyLuck", "DailyLuck"),
        ("goldenCoconutCracked", "GoldenCoconutCracked"),
    ):
        field(root, tag, baseline[key])
    player = ET.SubElement(root, "player")
    field(player, "name", "Reference player")
    field(player, "luckLevel", baseline["LuckLevel"])
    field(player, "miningLevel", baseline["MiningLevel"])
    stats = ET.SubElement(ET.SubElement(player, "stats"), "Values")
    for key, value in (
        ("daysPlayed", metadata["DaysPlayed"]),
        ("timesFished", metadata["TimesFished"]),
        ("ArtifactSpotsDug", baseline["Dug"]),
        ("mastery_0", int(baseline["FarmingMastery"])),
    ):
        entry = ET.SubElement(stats, "item")
        field(ET.SubElement(entry, "key"), "string", key)
        field(ET.SubElement(entry, "value"), "unsignedInt", value)
    hoe = ET.SubElement(ET.SubElement(player, "items"), "Item")
    field(hoe, "itemId", "Hoe")
    enchantments = ET.SubElement(hoe, "enchantments")
    for flag, kind in (
        ("Generous", "GenerousEnchantment"),
        ("Archaeologist", "ArchaeologistEnchantment"),
    ):
        if baseline[flag]:
            ET.SubElement(
                enchantments,
                "BaseEnchantment",
                {"{http://www.w3.org/2001/XMLSchema-instance}type": kind},
            )
    mail = ET.SubElement(player, "mailReceived")
    for flag in baseline["Mail"]:
        field(mail, "string", flag)
    orders = ET.SubElement(root, "specialOrders")
    for key in baseline["Orders"]:
        order = ET.SubElement(orders, "SpecialOrder")
        field(order, "questKey", key)
        field(order, "questState", "InProgress")
        field(order, "specialRule", ",".join(baseline["OrderRules"]))
    locations = ET.SubElement(root, "locations")
    for spot in baseline["Spots"]:
        location = ET.SubElement(locations, "GameLocation")
        field(location, "name", spot["Location"])
        field(location, "bridgeFixed", baseline["BridgeFixed"])
        entry = ET.SubElement(ET.SubElement(location, "objects"), "item")
        vector = ET.SubElement(ET.SubElement(entry, "key"), "Vector2")
        field(vector, "X", spot["X"])
        field(vector, "Y", spot["Y"])
        field(ET.SubElement(ET.SubElement(entry, "value"), "Object"), "itemId", "590")
    if not any(spot["Location"] == "IslandNorth" for spot in baseline["Spots"]):
        location = ET.SubElement(locations, "GameLocation")
        field(location, "name", "IslandNorth")
        field(location, "bridgeFixed", baseline["BridgeFixed"])
    path = tmp_path / "save.xml"
    path.write_bytes(ET.tostring(root))
    original_open, reads = Path.open, []

    def counted_open(self, *args, **kwargs):
        if self == path:
            reads.append(self)
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", counted_open)
    state = load_save(path)
    context = ArtifactState.from_game_state(state)
    assert asdict(
        artifact_predictor.predict(context, context.spots[0])
    ) == expected_result(case)
    assert reads == [path]
