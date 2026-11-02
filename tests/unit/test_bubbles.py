import gzip
import json
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

import pytest

from stardew.domain.predictions.bubbles import predict
from stardew.infrastructure.game_data.maps import read_maps
from stardew.resources import data_path

FIXTURES = Path(__file__).parents[1] / "fixtures"


def compressed(name):
    return json.loads(gzip.decompress((FIXTURES / (name + ".json.gz")).read_bytes()))


@pytest.fixture(scope="module")
def maps():
    return read_maps(data_path("maps.json"))


@pytest.mark.parametrize(
    "case",
    compressed("bubbles"),
    ids=lambda c: (
        f"{c['save']['Seed']}-{c['name']}-{c['save']['DaysPlayed']}-{c['save']['LegacyRandom']}-{c['panning']}"
    ),
)
def test_csharp_bubbles(case, maps):
    # These are outputs of the retired C# predictor, not the game. Its
    # frenzy, boundary and large-ID defects are covered by independent game
    # rule regressions in test_map_game_rules instead of preserved as truth.
    if abs(case["save"]["Seed"]) > 2**53:
        pytest.skip(
            "Legacy fixture used integer-exact seeds rather than the DLL's double conversion"
        )
    if case["name"] == "IslandNorth" and any(
        e["X"] in (0, 1) and 77 <= e["Y"] <= 80 for e in case["events"]
    ):
        pytest.skip(
            "Legacy geometry omitted map border zero; checked against installed-map evidence separately"
        )
    if any(e["Kind"] == "Frenzy" for e in case["events"]):
        pytest.skip(
            "Legacy unconditional frenzy is not a game oracle; session alternatives have independent tests"
        )
    # The old oracle ignored Year (always 2) and used the attempt count as a
    # Boolean eligibility flag. Give this arithmetic compatibility check a
    # coherent calendar and an explicit distinct-fish count with that flag;
    # real-save extraction and corrected eligibility are tested independently.
    saved = {SAVE_FIELDS[k]: v for k, v in case["save"].items()}
    saved["year"] = (saved["days_played"] - 1) // 112 + 1
    saved["fish_caught_count"] = 3 if saved["times_fished"] > 2 else 0
    assert [
        {k: v for k, v in asdict(e).items() if k != "scenario"}
        for e in predict(
            SimpleNamespace(**saved),
            case["name"],
            maps[case["name"]],
        )
    ] == [{EVENT_FIELDS[k]: v for k, v in e.items()} for e in case["events"]]


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
EVENT_FIELDS = {
    "Location": "location",
    "X": "x",
    "Y": "y",
    "Start": "start",
    "End": "end",
    "Kind": "kind",
}
