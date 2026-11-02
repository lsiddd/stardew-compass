"""Statues rules adapted from MouseyPounds (MIT; b9e7c71)."""

from stardew.domain.numeric import f32

from ..report_support import (
    SystemRandom,
    capture,
    exact_seed_part,
    floor,
    prediction_days,
    random_seed,
    trunc_div,
    trunc_rem,
)
from .calendar_rules import is_festival
from .weather import weather_for_day


def predict_statues(context, is_search=None, offset=None):
    save = context.save
    (
        bless_no_rain,
        bless_rain,
        blessing_names,
        coords,
        day,
        dwarf1,
        dwarf2,
        dwarf_names,
        i,
        index,
        j,
        map_dim,
        pb_maps,
        player,
        rng,
        roll,
        shard,
        _week,
        _week_day,
    ) = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )
    blessing_names = [
        "Speed",
        "Luck",
        "Energy",
        "Waters",
        "Friendship",
        "Fangs",
        "Butterfly",
    ]
    dwarf_names = ["+1 Ore", "Ladders", "Coal", "Bomb Immunity", "Geodes"]
    pb_maps = [
        "Forest",
        "Town",
        "Beach",
        "Mountain",
        "Secret Woods",
        "Bus Stop",
        "Backwoods",
    ]
    map_dim = [
        [120, 120],
        [130, 110],
        [104, 50],
        [135, 41],
        [60, 32],
        [65, 30],
        [50, 40],
    ]
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    for day in prediction_days(context, offset):
        game_day = day + save["dayAdjust"]
        festival = is_festival(game_day)
        weather, weather_source, _ = weather_for_day(save, game_day)
        raining = all(
            value in ("Rain", "Storm", "GreenRain", "Green Rain") for value in weather
        )
        rng = SystemRandom(
            random_seed(
                game_day,
                trunc_div(save["gameID"], 2),
                game_day * 777,
                legacy=save["useLegacyRandom"],
            )
        )
        j = 0
        while j < 8:
            rng.next()
            j += 1
        roll = rng.double()
        bless_rain = floor(roll * 6)
        bless_no_rain = floor(roll * (6 if festival else 7))
        if bless_no_rain == 6 and not raining:
            if "mp_ids" in save:
                player = 0
                while player < len(save.get("mp_ids")):
                    if (
                        context.selected_players is not None
                        and player not in context.selected_players
                    ):
                        player += 1
                        continue
                    rng = SystemRandom(
                        random_seed(
                            exact_seed_part(int(game_day)),
                            exact_seed_part(trunc_div(int(save.get("gameID")), 2)),
                            exact_seed_part(
                                trunc_rem(save.get("mp_ids")[int(player)], 10000)
                            ),
                            legacy=save["useLegacyRandom"],
                        )
                    )
                    shard = (
                        rng.double()
                        < f32(0.05)
                        + save.get(
                            "playerLuck", (save["dailyLuck"],) * len(save["mp_ids"])
                        )[player]
                    )
                    rng = SystemRandom(
                        random_seed(
                            exact_seed_part(int(game_day)),
                            exact_seed_part(trunc_div(int(save.get("gameID")), 2)),
                            exact_seed_part(
                                trunc_rem(save.get("mp_ids")[int(player)], 10000)
                            ),
                            legacy=save["useLegacyRandom"],
                        )
                    )
                    index = rng.next(len(pb_maps))
                    coords = []
                    i = 0
                    while i <= 32:
                        coords.append(
                            {
                                "x": rng.next(map_dim[int(index)][0]),
                                "y": rng.next(map_dim[int(index)][1]),
                            }
                        )
                        i += 1
                    capture(
                        context,
                        "predictStatues",
                        {
                            "day": day,
                            "player": player,
                            "index": index,
                            "shard": shard,
                            "pbMaps": pb_maps,
                            "coords": coords,
                            "spawnConditions": "Butterfly blessing active, before 17:00, current map dimensions unchanged, clear spawn tile",
                        },
                    )
                    player += 1
        rng = SystemRandom(
            random_seed(
                game_day * 77, save.get("gameID"), legacy=save["useLegacyRandom"]
            )
        )
        dwarf1 = rng.next(5)
        dwarf2 = dwarf1
        while dwarf2 == dwarf1:
            dwarf2 = rng.next(5)
        capture(
            context,
            "predictStatues",
            {
                "day": day,
                "blessRain": bless_rain,
                "blessNoRain": bless_no_rain,
                "dwarf1": dwarf1,
                "dwarf2": dwarf2,
                "blessingNames": blessing_names,
                "dwarfNames": dwarf_names,
                "isFestival": festival,
                "effectiveBlessing": blessing_names[
                    bless_rain if raining or festival else bless_no_rain
                ],
                "weatherAlternatives": weather,
                "weatherSource": weather_source,
                "conditions": "Requires farming mastery and an unused statue blessing today; future weather changes can alter the choice",
            },
        )
    return None
