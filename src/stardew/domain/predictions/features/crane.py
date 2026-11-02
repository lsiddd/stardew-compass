"""Crane rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    prediction_days,
    random_seed,
)


def predict_crane(context, is_search=None, offset=None):
    save = context.save
    day, rng, this_event, _week, _week_day = (None, None, None, None, None)
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    for day in prediction_days(context, offset):
        if compare_version(save.get("version"), "1.6") >= 0:
            rng = SystemRandom(
                random_seed(
                    save.get("gameID"),
                    day + save.get("dayAdjust") - 1,
                    legacy=save["useLegacyRandom"],
                )
            )
        else:
            rng = SystemRandom(save.get("gameID") + day + save.get("dayAdjust") - 1)
        game_day = day + save["dayAdjust"]
        first_entered = save.get("theaterDayFirstEntered")
        occupied = (
            compare_version(save.get("version"), "1.4") >= 0 and rng.double() < 0.25
        )
        availability = "available_before_movie"
        if first_entered == game_day - 1:
            occupied = True
            availability = "first_visit"
        if occupied:
            this_event = " (Game In Use)"
            if availability != "first_visit":
                availability = "occupied"
        elif first_entered is None or first_entered < 0:
            this_event = (
                "Unavailable on the first visit; otherwise playable before the movie"
            )
            availability = "conditional_first_visit"
        else:
            this_event = "Game Can Be Played \xa0"
        availability_if_built = availability
        if save.get("theaterBuilt") is False:
            this_event = (
                "Theater not built; projected availability: " + this_event.strip()
            )
            availability = "requires_theater"
        capture(
            context,
            "predictCrane",
            {
                "day": day,
                "thisEvent": this_event,
                "availability": availability,
                "availabilityIfBuilt": availability_if_built,
                "theaterBuilt": save.get("theaterBuilt"),
                "conditions": "Theater must be built; this is before watching the movie. The first-ever visit always occupies the machine",
            },
        )
    return None
