"""Train arrival rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    prediction_days,
    random_seed,
)
from .calendar_rules import INSTALLED_GAME_PROFILE, day_random, is_festival


def predict_trains(context, is_search=None, offset=None):
    save = context.save
    if offset is None:
        offset = 28 * (save["daysPlayed"] // 28)
    for day in prediction_days(context, offset):
        game_day = day + save["dayAdjust"]
        if compare_version(save["version"], "1.6") >= 0:
            seed = random_seed(
                day + save["dayAdjust"],
                save["gameID"] / 2,
                legacy=save["useLegacyRandom"],
            )
        else:
            seed = save["gameID"] / 2 + day + save["dayAdjust"]
        random = SystemRandom(seed)
        train_time = None
        verified_profile = save.get("game_profile") == INSTALLED_GAME_PROFILE
        first_accessible_day = 32 if verified_profile else 31
        description = (
            "Railroad not yet accessible"
            if game_day < first_accessible_day
            else "\xa0 (No train) \xa0"
        )
        candidate = None
        if game_day >= first_accessible_day and not is_festival(game_day):
            if verified_profile:
                # Railroad.ResetTrainForNewDay in the inspected DLL. Its
                # effective 9% arrival rate is derived from adjacent-day rolls.
                chance = (1 - (1 - 4 * 0.09) ** 0.5) / 2
                today = day_random(save, game_day).double()
                tomorrow = day_random(save, game_day + 1).double()
                if today < chance <= tomorrow:
                    candidate = 900
            elif random.double() < 0.2:
                candidate = random.next(900, 1800) // 10 * 10
        if candidate is not None:
            hour, minute = divmod(candidate, 100)
            if minute < 60:
                train_time = candidate
                description = f" Train at {hour - 12 if hour > 12 else hour}:{minute:02d}{' pm' if hour >= 12 else ' am'}"
        capture(
            context,
            "predictTrains",
            {
                "day": day,
                "thisTrain": description,
                "trainTime": train_time,
                "ruleProfile": save.get("game_profile") or "historical_vanilla",
                "verification": "matched_installed_dll"
                if verified_profile
                else "unverified_historical_rule",
            },
        )
