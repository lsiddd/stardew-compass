"""Night rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    floor,
    fmod,
    prediction_days,
)
from .calendar_rules import calendar_parts, day_random
from .weather import weather_for_day


def _current_event(save, waking_day, mature_fairy_rose):
    """Return the selected event candidate with the game's short-circuit draws."""
    rng = day_random(save, waking_day)
    for _ in range(10):
        rng.double()
    if waking_day in save.get("weddingDays", ()):
        return "(No event: wedding)", False
    if waking_day == 31:
        return "Earthquake", False
    if waking_day == (save.get("daysPlayed") or 0) + 1:
        pending = save.get("pendingNightEvents", ())
        if pending:
            return pending[0], False
    received = save.get("hostMailReceived", ())
    mail = save.get("hostMailWithPending", ())
    if (
        save.get("hostCcCeremonySeen")
        and "abandonedJojaMartAccessible" not in received
        and "ccMovieTheater" not in received
        and all(
            weather in ("Rain", "Storm", "GreenRain")
            for weather in weather_for_day(save, waking_day)[0]
        )
    ):
        return "Abandoned JojaMart opening", False
    if (
        all(
            flag in mail
            for flag in ("willyBoatTicketMachine", "willyBoatHull", "willyBoatAnchor")
        )
        and "willyBoatFixed" not in mail
    ):
        return "Boat repair", False
    if (
        "activateGoldenParrotsTonight" in mail
        and save.get("activatedGoldenParrot") is False
    ):
        return "Golden Parrot activation", False
    windstorm = bool(save.get("greenhouseUnlocked")) and rng.double() < 0.1
    if windstorm and save.get("raccoonTreeFallen") is False:
        return "Windstorm", True
    if save.get("sawQiPlane") is False and (
        save.get("gotFirstBillboardPrizeTicketAny") or waking_day > 50
    ):
        return "Qi Plane", False
    year, season, day_of_month = calendar_parts(waking_day)
    fairy_chance = 0.01 + (0.007 if mature_fairy_rose else 0)
    if rng.double() < fairy_chance and season != 3 and day_of_month != 1:
        return "Fairy", windstorm and not save.get("raccoonTreeFallen", False)
    if rng.double() < 0.01 and waking_day > 20:
        return "Witch", windstorm and not save.get("raccoonTreeFallen", False)
    if rng.double() < 0.01 and waking_day > 5:
        return "Meteor", windstorm and not save.get("raccoonTreeFallen", False)
    if rng.double() < 0.005:
        return "Stone Owl", windstorm and not save.get("raccoonTreeFallen", False)
    if rng.double() < 0.008 and year > 1 and not save.get("gotCapsule", False):
        return "Strange Capsule", windstorm and not save.get("raccoonTreeFallen", False)
    return "(No event)", windstorm and not save.get("raccoonTreeFallen", False)


def _predict_current_night(context, day):
    save = context.save
    waking_day = day + save["dayAdjust"] + 1
    rose = save.get("hasMatureFairyRoseTonight")
    # A saved runtime flag describes only the immediate night, not all future
    # crops. Future predictions retain both possible Fairy Rose conditions.
    if day + save["dayAdjust"] != save.get("daysPlayed"):
        rose = None
    outcomes = (False, True) if rose is None else (bool(rose),)
    candidates = []
    windstorm = False
    for has_rose in outcomes:
        event, possible_wind = _current_event(save, waking_day, has_rose)
        windstorm |= possible_wind
        candidates.append(
            {
                "event": event,
                "condition": "Mature Fairy Rose at bedtime"
                if has_rose
                else "No mature Fairy Rose at bedtime",
            }
        )
    names = tuple(dict.fromkeys(candidate["event"] for candidate in candidates))
    if len(names) == 1:
        candidates = [
            {
                "event": names[0],
                "condition": "Saved progression still applies at bedtime",
            }
        ]
    capture(
        context,
        "predictNight",
        {
            "day": day,
            "wakingDay": waking_day,
            "thisEvent": " or ".join(names),
            "eventCandidates": candidates,
            "couldBeWindstorm": windstorm,
            "certainty": "conditional",
            "conditions": (
                "Weddings, pending repairs, world changes and personal events may take priority",
                "Farm event setup still needs a valid target or clear tiles",
                "Future candidates use saved progression; capsule, windstorm and Qi Plane are one-time events",
            ),
        },
    )


def predict_night(context, is_search=None, offset=None):
    save = context.save
    (
        could_be_windstorm,
        day,
        month,
        rng,
        this_event,
        _week,
        _week_day,
        year,
    ) = (None, None, None, None, None, None, None, None)
    if offset is None:
        offset = 28 * floor(save.get("daysPlayed") / 28)
    month = floor(offset / 28)
    year = 1 + floor(offset / 112)
    for day in prediction_days(context, offset):
        if compare_version(save["version"], "1.6") >= 0:
            _predict_current_night(context, day)
            continue
        could_be_windstorm = False
        if day + save.get("dayAdjust") == 30:
            this_event = " Earthquake"
        else:
            rng = SystemRandom(save.get("gameID") / 2 + day + 1 + save.get("dayAdjust"))
            if (
                compare_version(save.get("version"), "1.3") < 0
                and save.get("canHaveChildren")
            ) and rng.double() < 0.05:
                this_event = ' "Want a Baby?"'
            elif rng.double() < 0.01 and fmod(month, 4) < 3:
                this_event = " Fairy"
            elif rng.double() < 0.01:
                this_event = " Witch"
            elif rng.double() < 0.01:
                this_event = " Meteor"
            elif compare_version(save.get("version"), "1.5") < 0:
                if rng.double() < 0.01 and year > 1:
                    this_event = " Strange Capsule"
                elif rng.double() < 0.01:
                    this_event = " Stone Owl"
                else:
                    this_event = "\xa0 (No event) \xa0"
            elif compare_version(save.get("version"), "1.5.3") < 0:
                if rng.double() < 0.008 and year > 1:
                    this_event = " Strange Capsule"
                elif rng.double() < 0.008:
                    this_event = " Stone Owl"
                else:
                    this_event = "\xa0 (No event) \xa0"
            elif rng.double() < 0.005:
                this_event = " Stone Owl"
            elif rng.double() < 0.008 and year > 1:
                this_event = " Strange Capsule"
            else:
                this_event = "\xa0 (No event) \xa0"
        capture(
            context,
            "predictNight",
            {
                "day": day,
                "thisEvent": this_event,
                "couldBeWindstorm": could_be_windstorm,
            },
        )
    return None
