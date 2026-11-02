"""Plan calculation pages without mixing day, year and sequence offsets."""

from collections.abc import Mapping
from typing import Any

from .registry import Feature, day_window
from .report_models import ReportPredictionOptions
from .report_support import compare_version

CALENDAR_FEATURES = frozenset(
    ("mines", "trash", "train", "night", "crane", "greenrain", "statue")
)
WEEKLY_FEATURES = frozenset(("cart", "krobus", "sandy", "wallpaper"))


def calculation_offsets(
    feature: Feature,
    save: Mapping[str, Any],
    options: ReportPredictionOptions,
    player: int,
) -> tuple[int | None, ...]:
    if feature.range_kind == "sequence":
        if options.start is not None:
            return (options.start - 1,)
        counter = save[feature.counter]
        return (counter[player] if isinstance(counter, (tuple, list)) else counter,)
    if feature.range_kind == "fixed":
        return (None,)
    if feature.range_kind == "years":
        first = (options.start or save["year"]) - 1
        if options.start is None and save["daysPlayed"] is not None:
            last_festival_day = {"makeover": 17, "winterstar": 109}[feature.identifier]
            first = (save["daysPlayed"] - 1) // 112
            if save["daysPlayed"] > first * 112 + last_festival_day:
                first += 1
        return tuple(range(first, first + (options.count or 1)))
    if feature.range_kind == "games":
        return (options.start,)
    window = day_window(feature, save["daysPlayed"], options.start, options.count)
    assert window is not None
    if feature.identifier == "mines":
        return (None,)
    width = feature.page_size
    first = (window.start - 1) // width * width
    offsets = set(range(first, window.stop - 1, width))
    if feature.identifier == "cart":
        festival_days = (
            (10, 94)
            if compare_version(save["version"], "1.6") >= 0
            else (94,)
            if compare_version(save["version"], "1.3") >= 0
            else ()
        )
        for year in range(first // 112, window.stop // 112 + 1):
            offsets.update(
                year * 112 + day
                for day in festival_days
                if window.start < year * 112 + day + 8
                and window.stop > year * 112 + day + 5
            )
    return tuple(sorted(offsets))


def calculation_offset(
    feature: Feature, saved_day: int | None, offset: int | None
) -> int:
    if offset is not None:
        return offset
    if feature.identifier == "book":
        return 28 * (saved_day // 28)
    if feature.identifier in WEEKLY_FEATURES:
        return 7 * ((saved_day - 1) // 7)
    return 0
