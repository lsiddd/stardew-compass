"""Weather rules, separating seeded outcomes from session-dependent subtypes.

Initial calendar rules adapted from MouseyPounds (MIT; b9e7c71). Conditions
checked against the installed 1.6.15 LocationContexts data and game methods.
"""

from stardew.domain.numeric import f32

from ..report_support import (
    SystemRandom,
    capture,
    hash_string,
    prediction_days,
    random_seed,
)
from .calendar_rules import (
    PASSIVE_VALLEY_FESTIVAL_DAYS,
    calendar_parts,
    day_random,
    is_festival,
)


def weather_for_day(save, day):
    """Return possible weather without inventing the unsaved Game1.random state."""
    year, season, day_of_month = calendar_parts(day)
    rng = SystemRandom(
        random_seed(year * 777, save["gameID"], legacy=save["useLegacyRandom"])
    )
    green_rain_day = (5, 6, 7, 14, 15, 16, 18, 23)[rng.next(8)]
    saved = save.get("weatherOverrides", {}).get(str(day))
    if saved is None:
        saved = save.get("weatherOverrides", {}).get(day)
    # Today's weather was already resolved by UpdateWeatherForNewDay. The
    # saved weatherForTomorrow is still subject to that method's calendar
    # modifications when the next day starts.
    if saved is not None and day == save.get("daysPlayed"):
        return (saved,), "saved", green_rain_day
    if day in save.get("weddingDays", ()):
        return ("Wedding",), "saved_calendar", green_rain_day
    if is_festival(day):
        return ("Festival",), "calendar", green_rain_day
    if (day - 1) % 112 + 1 in PASSIVE_VALLEY_FESTIVAL_DAYS:
        return ("Sun",), "calendar", green_rain_day
    if day_of_month == 1 or day in (1, 2, 4):
        return ("Sun",), "calendar", green_rain_day
    if day == 3:
        return ("Rain",), "calendar", green_rain_day
    if season == 1:
        if day_of_month == green_rain_day:
            return ("GreenRain",), "seeded", green_rain_day
        if day_of_month % 13 == 0:
            return ("Storm",), "calendar", green_rain_day
    if saved is not None:
        return (saved,), "saved", green_rain_day
    if season == 1:
        chance = f32(f32(0.12) + f32((day_of_month - 1) * f32(0.003)))
        rain = (
            day_random(save, day - 1, hash_string("summer_rain_chance")).double()
            < chance
        )
        return (("Rain", "Storm") if rain else ("Sun",)), "seeded", green_rain_day
    rng = SystemRandom(
        random_seed(
            hash_string("location_weather"),
            save["gameID"],
            day - 1,
            legacy=save["useLegacyRandom"],
        )
    )
    if season == 3:
        return (
            (("Snow",) if rng.double() < f32(0.63) else ("Sun",)),
            "seeded",
            green_rain_day,
        )
    if rng.double() < f32(0.183):
        alternatives = (
            ("Rain", "Storm")
            if day - 1 >= 28 and day_of_month not in (2, 3)
            else ("Rain",)
        )
    else:
        alternatives = ("Sun", "Wind") if day - 1 >= 3 else ("Sun",)
    return alternatives, "seeded", green_rain_day


def predict_green_rain(context, is_search=None, offset=None):
    save = context.save
    if offset is None:
        offset = 28 * (save["daysPlayed"] // 28)
    for day in prediction_days(context, offset):
        game_day = day + save["dayAdjust"]
        alternatives, source, green_rain_day = weather_for_day(save, game_day)
        capture(
            context,
            "predictGreenRain",
            {
                "day": day,
                "weatherTown": " or ".join(alternatives),
                "weatherAlternatives": alternatives,
                "certainty": "session_dependent"
                if len(alternatives) > 1
                else "deterministic",
                "source": source,
                "assumptions": ()
                if source == "saved"
                else ("No future rain totem, wedding or modified weather data",),
                "greenRainDay": green_rain_day,
                "season": calendar_parts(game_day)[1],
            },
        )
