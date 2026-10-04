import gzip
import json
from pathlib import Path
import pytest
from stardew.domain.numeric import Random, xxhash32, div, rem, i32, f32

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
    "game_id,a,b,days,legacy,expected",
    [
        (
            -9223372036854775808,
            2147483647,
            -2147483648,
            2147483647,
            False,
            [100361328, 291571099, 1482220885, 1818653750],
        ),
        (
            -9223372036854775808,
            2147483647,
            -2147483648,
            2147483647,
            True,
            [1655911537, 867932563, 356479430, 2115372437],
        ),
        (
            9223372036854775807,
            2147483647,
            -2147483647,
            1,
            False,
            [658063156, 926577337, 2136960259, 1997153972],
        ),
        (
            9223372036854775807,
            2147483647,
            -2147483647,
            1,
            True,
            [534011718, 237820880, 1002897798, 1657007234],
        ),
        (-7, 0, 0, 1, False, [594704787, 350520523, 1772110364, 28116188]),
        (-7, 0, 0, 1, True, [1655911537, 867932563, 356479430, 2115372437]),
    ],
)
def test_map_seed_large_ids_and_extra_part_boundary(
    game_id, a, b, days, legacy, expected
):
    from types import SimpleNamespace
    from stardew.domain.numeric import for_day

    state = SimpleNamespace(game_id=game_id, days_played=days, use_legacy_random=legacy)
    random = for_day(state, a, b)
    assert [random.next() for _ in range(4)] == expected


def test_report_fractional_seed_coercion_and_negative_floor():
    from stardew.domain.numeric import int32, random_seed, SystemRandom

    assert int32(-3.9) == -3
    assert int32(10**1000 + 7) == 7
    assert random_seed(-3.5, 1, legacy=True) == -3
    assert SystemRandom(-3.5).next() == SystemRandom(-3).next()
