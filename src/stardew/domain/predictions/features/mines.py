"""Mines rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    fmod,
    random_seed,
)
from .calendar_rules import day_random


def _layout(save, day, level, lowest):
    """The regular-mine portion of MineShaft.loadLevel's layout selection."""
    layout = level % 40
    alternate_exclusion = False
    if (
        compare_version(save["version"], "1.6.4") >= 0
        and lowest is not None
        and lowest >= 120
        and layout != 10
        and layout % 5
        and level > 1
    ):
        rng = day_random(save, day, 1293857 + level * 400)
        if rng.double() < 0.06:
            special = (40, 47, 50, 51)
            layout = rng.next(40, 61)
            if layout in special and rng.double() < 0.75:
                layout = rng.next(40, 61)
            if layout == 53:
                layout = rng.next(52, 61)
            if layout == 40 and 40 < level <= 80:
                layout = rng.next(52, 61)
            alternate_exclusion = layout in special
    return layout, alternate_exclusion


def _floor_type(save, day, level, layout, alternate_exclusion, monster_musk):
    rng = day_random(save, day, level * 100)
    if (
        not monster_musk
        and rng.double() < 0.044
        and layout % 5 != 0
        and 5 < layout % 40 < 30
        and layout % 40 != 19
        and not alternate_exclusion
    ):
        return "monster" if rng.double() < 0.5 else "slime"
    if (
        rng.double() < 0.044
        and save.get("quarryUnlocked")
        and save.get("quarryMineVisited")
        and layout % 40 > 1
        and layout % 5 != 0
    ):
        return "quarry"
    return None


def _current_mines(context, day):
    save = context.save
    game_day = day + save["dayAdjust"]
    order_level = save.get("lowestMineLevelForOrder")
    lowest = (
        order_level
        if order_level is not None and order_level >= 0
        else save.get("lowestMineLevel")
    )
    musk = save.get("anyOnlineFarmerHasMonsterMusk")
    kinds = {"monster": [], "slime": [], "quarry": []}
    with_musk = {"monster": [], "slime": [], "quarry": [], "rainbowLights": []}
    rainbow_lights = []
    alternate_layouts = {}
    for level in range(1, 120):
        if level % 5 == 0:
            continue
        layout, excluded = _layout(save, game_day, level, lowest)
        if layout != level % 40:
            alternate_layouts[str(level)] = layout
        kind = _floor_type(save, game_day, level, layout, excluded, musk is True)
        if kind is not None:
            kinds[kind].append(level)
        if musk is None:
            alternative = _floor_type(save, game_day, level, layout, excluded, True)
            if alternative is not None:
                with_musk[alternative].append(level)
        rng = day_random(save, game_day, game_day, level, 4 * level)
        if not save.get("hardmodeMines") and rng.double() < 0.3 and level > 2:
            rng.double()
        rng.double()
        if rng.double() < 0.035 and level > 80:
            # Quarry floors override their original mine area, which disables
            # mushroom lighting even though the lighting RNG still runs.
            if kind != "quarry":
                rainbow_lights.append(level)
            if musk is None and alternative != "quarry":
                with_musk["rainbowLights"].append(level)
    dino_candidates = []
    for level in range(127, 621):
        if level in (220, 320, 420):
            continue
        rng = day_random(save, game_day, level * 100)
        if rng.double() < 0.044:
            rng.double()
            if rng.double() < 0.5:
                dino_candidates.append(level - 120)
    capture(
        context,
        "predictMines",
        {
            "day": day,
            "rainbowLights": rainbow_lights,
            "infestedMonster": kinds["monster"],
            "infestedSlime": kinds["slime"],
            "quarryLevel": kinds["quarry"],
            "dinoLevel": dino_candidates,
            "dinoLevelCertainty": "candidates_only",
            "dinoLevelConditions": "Eligible generated map, no treasure-room replacement; session generation RNG is unavailable",
            "alternateLayouts": alternate_layouts,
            "monsterMusk": musk,
            "monsterMuskAlternative": with_musk if musk is None else {},
            "assumptions": (
                "No forced map layout or mods",
                "Mushroom candidates require first generation of that floor today",
                *(
                    ("Base layout scenario: global mine progress is missing",)
                    if lowest is None
                    else ()
                ),
                *(
                    (
                        "Main floor lists assume no online farmer has Monster Musk; alternative lists show its effect",
                    )
                    if musk is None
                    else ()
                ),
            ),
        },
    )


def predict_mines(context, is_search=None, offset=None):
    """Predict independent days, preserving every per-floor random draw."""
    save = context.save
    before_14 = compare_version(save["version"], "1.4") < 0
    before_15 = compare_version(save["version"], "1.5") < 0
    before_16 = compare_version(save["version"], "1.6") < 0
    if context.day_range is not None:
        days = range(*context.day_range)
    else:
        if offset is None:
            offset = 28 * floor(save["daysPlayed"] / 28)
        days = range(offset + 1, offset + 29)
    for day in days:
        if not before_16:
            _current_mines(context, day)
            continue
        rainbow_lights = []
        infested_monster = []
        infested_slime = []
        quarry_level = []
        dino_level = []
        if before_14:
            mine_level = 1
            while mine_level < 120:
                if fmod(mine_level, 5) == 0:
                    mine_level += 1
                    continue
                rng = SystemRandom(
                    day + save.get("dayAdjust") + mine_level + save.get("gameID") / 2
                )
                if (fmod(mine_level, 40) > 5 and fmod(mine_level, 40) < 30) and fmod(
                    mine_level, 40
                ) != 19:
                    if rng.double() < 0.044:
                        if rng.double() < 0.5:
                            infested_monster.append(mine_level)
                        else:
                            infested_slime.append(mine_level)
                        mine_level += 1
                        continue
                rng = SystemRandom(
                    day + save.get("dayAdjust") + mine_level + save.get("gameID") / 2
                )
                if rng.double() < 0.3 and mine_level > 2:
                    rng.double()
                rng.double()
                if rng.double() < 0.035 and mine_level > 80:
                    rainbow_lights.append(mine_level)
                mine_level += 1
        else:
            mine_level = 1
            while mine_level < 120:
                skip_mushroom_check = False
                if fmod(mine_level, 5) == 0:
                    mine_level += 1
                    continue
                if before_16:
                    rng = SystemRandom(
                        day
                        + save.get("dayAdjust")
                        + mine_level * 100
                        + save.get("gameID") / 2
                    )
                else:
                    rng = SystemRandom(
                        random_seed(
                            day + save.get("dayAdjust"),
                            save.get("gameID") / 2,
                            mine_level * 100,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                if (
                    (rng.double() < 0.044 and fmod(mine_level, 40) > 5)
                    and fmod(mine_level, 40) < 30
                ) and fmod(mine_level, 40) != 19:
                    if rng.double() < 0.5:
                        infested_monster.append(mine_level)
                    else:
                        infested_slime.append(mine_level)
                    skip_mushroom_check = True
                elif (rng.double() < 0.044 and save.get("quarryUnlocked")) and fmod(
                    mine_level, 40
                ) > 1:
                    if rng.double() < 0.25 and before_15:
                        quarry_level.append(f"{mine_level}*")
                    else:
                        quarry_level.append(mine_level)
                    skip_mushroom_check = True
                if skip_mushroom_check:
                    mine_level += 1
                    continue
                if before_16:
                    rng = SystemRandom(
                        (day + save.get("dayAdjust")) * mine_level
                        + 4 * mine_level
                        + save.get("gameID") / 2
                    )
                else:
                    rng = SystemRandom(
                        random_seed(
                            day + save.get("dayAdjust"),
                            save.get("gameID") / 2,
                            day + save.get("dayAdjust"),
                            mine_level,
                            4 * mine_level,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                if not save.get("hardmodeMines"):
                    if rng.double() < 0.3 and mine_level > 2:
                        rng.double()
                rng.double()
                if rng.double() < 0.035 and mine_level > 80:
                    rainbow_lights.append(mine_level)
                mine_level += 1
            mine_level = 127
            while mine_level < 621:
                if before_16:
                    rng = SystemRandom(
                        day
                        + save.get("dayAdjust")
                        + mine_level * 100
                        + save.get("gameID") / 2
                    )
                else:
                    rng = SystemRandom(
                        random_seed(
                            day + save.get("dayAdjust"),
                            save.get("gameID") / 2,
                            mine_level * 100,
                            legacy=save["useLegacyRandom"],
                        )
                    )
                if rng.double() < 0.044:
                    not rng.double() < 0.5
                    if rng.double() < 0.5:
                        dino_level.append(mine_level - 120)
                mine_level += 1
        capture(
            context,
            "predictMines",
            {
                "day": day,
                "rainbowLights": rainbow_lights,
                "infestedMonster": infested_monster,
                "infestedSlime": infested_slime,
                "quarryLevel": quarry_level,
                "dinoLevel": dino_level,
            },
        )
