from dataclasses import asdict
import gzip
import json
from pathlib import Path
import pytest
from types import SimpleNamespace
from stardew.infrastructure.game_data.maps import read_maps
from stardew.domain.predictions.bubbles import predict
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
    assert [
        asdict(e)
        for e in predict(
            SimpleNamespace(**{SAVE_FIELDS[k]: v for k, v in case["save"].items()}),
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
