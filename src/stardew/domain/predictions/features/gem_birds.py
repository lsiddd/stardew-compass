"""Gem Birds rules adapted from MouseyPounds (MIT; b9e7c71)."""

from ..report_support import (
    SystemRandom,
    capture,
    compare_version,
    random_seed,
    set_slot,
)


def predict_gem_birds(context, is_search=None, offset=None):
    save = context.save
    birds, gems, i, j, locs, rng, temp = (None, None, None, None, None, None, None)
    birds = ["Green", "Blue", "Red", "Purple", "Brown"]
    gems = {
        "Green": "Emerald",
        "Blue": "Aquamarine",
        "Red": "Ruby",
        "Purple": "Amethyst",
        "Brown": "Topaz",
    }
    locs = [
        "North (Dig Site / Volcano)",
        "South (Docks / Resort)",
        "East (Jungle)",
        "West (Farm)",
    ]
    if compare_version(save.get("version"), "1.6") >= 0:
        rng = SystemRandom(
            random_seed(save.get("gameID"), legacy=save["useLegacyRandom"])
        )
    else:
        rng = SystemRandom(save.get("gameID"))
    i = len(birds)
    while i > 1:
        j = rng.next((i := (i + -1)) - -1)
        temp = birds[int(i)]
        set_slot(birds, i, birds[int(j)])
        set_slot(birds, j, temp)
    i = 0
    while i < len(locs):
        capture(
            context,
            "predictGemBirds",
            {"i": i, "locs": locs, "birds": birds, "gems": gems},
        )
        i += 1
    return None
