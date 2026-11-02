import gzip
import json
from pathlib import Path

import pytest

from stardew.domain.numeric import Random, div, f32, i32, rem, xxhash32

FIXTURES = Path(__file__).parents[1] / "fixtures"


def compressed(name):
    return json.loads(gzip.decompress((FIXTURES / (name + ".json.gz")).read_bytes()))


@pytest.mark.parametrize(
    "hex,expected",
    [
        ("", 0x02CC5D05),
        ("61", 0x550D7456),
        ("616263", 0x32D153FF),
        ("000102030405060708090a0b0c0d0e0f10111213", 0x828B819C),
        ("7000000001a0a60b620200008200000000000000", 0x98C2CF7A),
    ],
)
def test_independent_hash_vectors(hex, expected):
    assert xxhash32(bytes.fromhex(hex)) == expected


@pytest.mark.parametrize("case", compressed("random"), ids=lambda c: str(c["seed"]))
def test_mixed_system_random(case):
    r = Random(case["seed"])
    assert [
        [
            r.next(),
            r.double(),
            r.next(100),
            r.next(-100, 100),
            r.next(-(2**31), 2**31 - 1),
            r.next(0),
            r.next(3, 3),
        ]
        for _ in range(20)
    ] == case["values"]


def test_integer_and_single_semantics():
    assert div(-7, 2) == -3 and rem(-7, 2) == -1
    assert div(7, -2) == -3 and rem(7, -2) == 1
    assert i32(2**31) == -(2**31)
    assert f32(0.1) == 0.10000000149011612
    with pytest.raises(ValueError):
        Random(0).next(-1)
    with pytest.raises(ValueError):
        Random(0).next(2, 1)


@pytest.mark.parametrize(
    "case",
    json.loads((FIXTURES / "game-seed-boundaries.json").read_text(encoding="utf-8"))[
        "cases"
    ],
    ids=lambda case: f"{case['game_id']}_{case['legacy']}",
)
def test_game_dll_seed_boundaries(case):
    """Oracle is the installed Utility.CreateRandom, not a second predictor."""
    from types import SimpleNamespace

    from stardew.domain.numeric import for_day

    state = SimpleNamespace(
        game_id=case["game_id"],
        days_played=case["days"],
        use_legacy_random=case["legacy"],
    )
    random = for_day(state, case["a"], case["b"])
    assert [random.next() for _ in range(4)] == case["draws"]


def test_game_fractional_seed_coercion_truncates_toward_zero():
    from stardew.domain.numeric import SystemRandom, int32, random_seed

    assert int32(-3.9) == -3
    assert int32(10**1000 + 7) == 7
    assert random_seed(-3.5, 1, legacy=True) == -2
    assert SystemRandom(-3.5).next() == SystemRandom(-3).next()
