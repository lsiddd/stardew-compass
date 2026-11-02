"""Calico Jack rules adapted from MouseyPounds (MIT; b9e7c71)."""

from math import floor

from stardew.domain.numeric import f32

from ..report_support import SystemRandom, capture, compare_version, random_seed


class _Draws:
    """Replay alternative decisions against the same lazily generated draws."""

    def __init__(self, rng):
        self.rng = rng
        self.values = []

    def __getitem__(self, index):
        while index >= len(self.values):
            self.values.append(self.rng.double())
        return self.values[index]


def _dealer_result(draws, start, player, index, chance):
    total = start
    multiplier = 1
    super_roll = None
    while total < 18 or total < player:
        card = floor(9 * draws[index]) + 1
        index += 1
        distance = 21 - total
        auto_bust = False
        if player in (18, 19, 20):
            auto_bust = draws[index] < {18: 0.1, 19: 0.25, 20: 0.5}[player]
            index += 1
        if auto_bust:
            card = distance + floor(3 * draws[index]) + 1
            index += 1
        if draws[index] < chance:
            card = 999
            multiplier *= 3
            super_roll = draws[index]
        index += 1
        total += card
    return total, multiplier, super_roll


def _advice(plan):
    hits = plan["hits"]
    if plan["outcome"] == "loss":
        return "LOSS (Unavoidable)"
    if plan["action"] == "reach_21":
        return f"WIN: Hit {hits} time{'' if hits == 1 else 's'} to reach 21"
    prefix = "WIN" if plan["outcome"] == "win" else "TIE"
    if hits == 0 and prefix == "WIN":
        advice = f"WIN: Stand at initial {plan['player_total']}"
    else:
        advice = f"{prefix}: Hit {hits} time{'' if hits == 1 else 's'} and stand at {plan['player_total']}"
    if plan["winnings_multiplier"] == 3:
        confidence = (
            "Guaranteed" if plan["super_bust_roll"] < 0.0005 else "Luck-dependent"
        )
        advice += f"; {confidence} super bust with 3x winnings"
    return advice


def predict_calico_jack(context, is_search=None, offset=None, game_offset=0):
    save = context.save
    if offset is None:
        offset = save["daysPlayed"] + save["dayAdjust"]
    chance = max(
        0.0005,
        0.001 + save["dailyLuck"] / 20 + f32(f32(save["luckLevel"]) * f32(0.002)),
    )
    for num_played in range(game_offset + 1, game_offset + (context.count or 20) + 1):
        seed = (
            random_seed(
                num_played, offset, save["gameID"], legacy=save["useLegacyRandom"]
            )
            if compare_version(save["version"], "1.6") >= 0
            else num_played + offset + save["gameID"]
        )
        rng = SystemRandom(seed)
        dealer_start = rng.next(1, 12) + rng.next(1, 10)
        first, second = rng.next(1, 12), rng.next(1, 10)
        player_total = first + second
        draws = _Draws(rng)
        choices = []
        index = hits = 0
        while player_total < 21:
            choices.append({"t": player_total, "r": index, "h": hits})
            card = floor(9 * draws[index]) + 1
            index += 1
            distance = 21 - player_total
            if 1 < distance < 6:
                adjust = draws[index] < 1 / distance
                index += 1
                if adjust:
                    card = distance if draws[index] < 0.5 else distance - 1
                    index += 1
            player_total += card
            hits += 1
        plan = {
            "outcome": "loss",
            "action": None,
            "hits": None,
            "player_total": None,
            "dealer_total": None,
            "winnings_multiplier": 1,
            "super_bust_roll": None,
        }
        if player_total == 21:
            plan.update(outcome="win", action="reach_21", hits=hits, player_total=21)
        else:
            for choice in choices:
                dealer, multiplier, super_roll = _dealer_result(
                    draws, dealer_start, choice["t"], choice["r"], chance
                )
                if dealer > 21 or dealer == choice["t"] and plan["outcome"] == "loss":
                    plan.update(
                        outcome="win" if dealer > 21 else "tie",
                        action="stand",
                        hits=choice["h"],
                        player_total=choice["t"],
                        dealer_total=dealer,
                        winnings_multiplier=multiplier,
                        super_bust_roll=super_roll,
                    )
                    if dealer > 21:
                        break
        capture(
            context,
            "predictCalicoJack",
            {
                "numPlayed": num_played,
                "startHand": f"{first} and {second}",
                "dealerStart": dealer_start,
                "choice": choices,
                "advice": _advice(plan),
                "chance": chance,
                "plan": plan,
                "conditions": "Match the actual daily luck, luck level and number of Calico Jack games played in this session",
            },
        )
