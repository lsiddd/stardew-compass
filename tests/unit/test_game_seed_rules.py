"""Installed DLL seed vectors and audited festival rules, without a private save.

Seed/cactus values were captured from unmodified Utility methods in the DLL
identified in game-seed-boundaries.json. Winter Star checks use the inspected
GetRandomNpc algorithm and bundled base-game NPC pool.
"""

import pytest

from stardew.api import load_game_data
from stardew.domain.numeric import random_seed
from stardew.domain.predictions.features.festival import makeover_pool, predict_makeover
from stardew.domain.predictions.features.winter_star import predict_winter_star
from stardew.domain.predictions.report_support import PredictionContext, exact_seed_part

PLAYER_ID = -2062291679424207820


@pytest.fixture
def context():
    catalogs = load_game_data(include_maps=False).catalogs
    return PredictionContext(
        {
            "gameID": 390938626,
            "version": "1.6.15",
            "year": 2,
            "useLegacyRandom": False,
            "mp_ids": [PLAYER_ID],
            "names": ["Synthetic"],
            "gender": ["Male"],
            "leoMoved": False,
            "characters": list(catalogs["predictor_characters"]),
            "shirts": catalogs["predictor_shirts"],
        },
        catalogs,
    )


@pytest.mark.parametrize(
    "legacy,winter,prize,enchant",
    [
        (False, 2111593707, -609742824, -2039119640),
        (True, -1290384051, -1094914740, -1094914740),
    ],
)
def test_double_conversion_precedes_modulo_for_long_player_ids(
    legacy, winter, prize, enchant
):
    assert exact_seed_part(PLAYER_ID) == -1485853366
    assert random_seed(390938626 // 2, 2, PLAYER_ID, legacy=legacy) == winter
    assert random_seed(390938626, PLAYER_ID, legacy=legacy) == prize
    assert random_seed(0, 390938626, PLAYER_ID, legacy=legacy) == enchant


@pytest.mark.parametrize("legacy,parts", [(False, [18, 4, 6]), (True, [6, 19, 13])])
def test_cactus_uses_both_game_seed_calls(context, legacy, parts):
    context.save["useLegacyRandom"] = legacy
    predict_makeover(context, offset=1)
    assert next(f["parts"] for _, f in context.captures if "parts" in f) == parts


def test_winter_star_removes_recipient_before_donor_draw(context):
    predict_winter_star(context, offset=1)
    facts = context.captures[0][1]
    assert facts["secretSantaGiveTo"] == "Leah"
    assert facts["secretSantaGetFrom"] == "Kent"


def test_winter_star_divorce_filters_donor_only(context):
    context.save["divorcedNpcs"] = [("Kent", "Leah")]
    predict_winter_star(context, offset=1)
    facts = context.captures[0][1]
    assert facts["secretSantaGiveTo"] == "Leah"
    assert facts["secretSantaGetFrom"] not in {"Kent", "Leah"}


def test_makeover_filters_equipped_shirt_before_draw(context):
    assert len(makeover_pool(context, 0)) == 47
    context.save["equippedMakeoverItems"] = [(("shirtItem", "1017", "Shirt"),)]
    choices = makeover_pool(context, 0)
    assert len(choices) == 46
    assert all(choice["item_ids"].get("shirt") != "(S)1017" for choice in choices)


def test_makeover_uses_exported_order_and_part_gender(context):
    context.save["makeoverOutfits"] = [
        {"Gender": 1, "OutfitParts": [{"Id": "female", "ItemId": "(S)1"}]},
        {
            "Gender": None,
            "OutfitParts": [
                {"Id": "wrong-gender", "ItemId": "(S)2", "Gender": 1},
                {"Id": "first", "ItemId": "(S)3", "Gender": 0},
            ],
        },
        {"Gender": 0, "OutfitParts": [{"Id": "equipped", "ItemId": "(S)4"}]},
        {
            "Gender": 0,
            "OutfitParts": [{"Id": "last", "ItemId": "(S)5", "Color": "142 1 1"}],
        },
    ]
    context.save["equippedMakeoverItems"] = [(("shirtItem", "4", "Synthetic"),)]
    choices = makeover_pool(context, 0)
    assert [choice["shirt"] for choice in choices] == ["first", "last"]
    assert choices[-1]["colors"]["shirt"] == "#8e0101"


@pytest.mark.parametrize("legacy,expected", [(False, -1848363276), (True, 0)])
def test_seed_addition_uses_csharp_left_to_right_rounding(legacy, expected):
    # Captured by Utility.CreateRandomSeed. Python >=3.12 sum() returns a
    # compensated result here and would cross the integer truncation boundary.
    assert random_seed(1e9, 1e-8, -1e9, 0.999999999, legacy=legacy) == expected
