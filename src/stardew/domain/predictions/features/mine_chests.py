"""Normal and remixed mine rewards, adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import SystemRandom, capture, compare_version, int32, random_seed

_REWARDS = {
    10: ("(B)506", "(B)507", "(W)12", "(W)17", "(W)22", "(W)31"),
    20: ("(W)11", "(W)24", "(W)20", "(O)517", "(O)519"),
    30: (None,),
    40: ("(W)32",),
    50: ("(B)509", "(B)510", "(B)508", "(W)1", "(W)43"),
    60: ("(W)21", "(W)44", "(W)6", "(W)18", "(W)27"),
    70: ("(W)33",),
    80: ("(B)512", "(B)511", "(W)10", "(W)7", "(W)46", "(W)19"),
    90: ("(W)8", "(W)52", "(W)45", "(W)5", "(W)60"),
    100: ("(O)434",),
    110: ("(B)514", "(B)878", "(W)50", "(W)28"),
    120: ("Skull Key",),
}


def _name(save, item_id):
    if item_id is None:
        return "(No chest)"
    if item_id == "Skull Key":
        return item_id
    prefix, key = item_id[1], item_id[3:]
    if prefix in ("W", "B"):
        return save["weapons" if prefix == "W" else "boots"][key]
    return save["objects"]["_" + key]["name"]


def predict_mine_chests(context, is_search=None, offset=None):
    save = context.save
    mode = save.get("shuffleMineChests")
    for level, choices in _REWARDS.items():
        if compare_version(save["version"], "1.6") >= 0:
            # Utility.GetReplacementChestItem converts the game ID to double
            # before multiplying. Preserve that order for large IDs as well.
            seed = random_seed(
                float(save["gameID"]) * 512, level, legacy=save["useLegacyRandom"]
            )
        else:
            seed = int32(int(save["gameID"]) * 512 + level)
        remixed = choices[SystemRandom(seed).next(len(choices))]
        default = choices[0]
        known = mode in ("Default", "Remixed")
        selected = remixed if mode == "Remixed" else default
        # A missing mode is not a license to assume that remixed was selected.
        item = _name(save, selected) if known or default == remixed else None
        capture(
            context,
            "predictMineChests",
            {
                "floor": level,
                "item": item,
                "item_id": selected if item and selected != "Skull Key" else None,
                "rewardMode": mode if known else "unknown",
                "rewardAlternatives": ()
                if known or default == remixed
                else (
                    {
                        "mode": "Default",
                        "item_id": default,
                        "item": _name(save, default),
                    },
                    {
                        "mode": "Remixed",
                        "item_id": remixed,
                        "item": _name(save, remixed),
                    },
                ),
                "availability": "original_reward_not_remaining_chest",
                "availabilityCondition": "Reward not already collected by this player; Skull Key also requires no existing key",
            },
        )
