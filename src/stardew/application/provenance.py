"""Record assumptions and requested coverage alongside reproducible results."""

from stardew import __version__
from stardew.domain.models.state import freeze
from stardew.domain.predictions.registry import REGISTRY
from stardew.domain.predictions.report_models import ReportPredictionOptions
from stardew.domain.progress import PROGRESS_SECTIONS


def analysis_provenance(state, data, options, predictions):
    settings = options.prediction_options or ReportPredictionOptions()
    indices = (
        settings.player_indices
        if settings.player_indices is not None
        else tuple(range(len(state.players)))
    )
    coverage = {}
    for section in predictions:
        dates = [record.date.days_played for record in section.records if record.date]
        sequences = [
            record.sequence for record in section.records if record.sequence is not None
        ]
        coverage[section.section_id] = {
            "scope": REGISTRY[section.section_id].scope,
            "range_kind": REGISTRY[section.section_id].range_kind,
            "available": section.available,
            "records": len(section.records),
            "first_day": min(dates) if dates else None,
            "last_day": max(dates) if dates else None,
            "first_sequence": min(sequences) if sequences else None,
            "last_sequence": max(sequences) if sequences else None,
        }
    return freeze(
        {
            **data.provenance,
            "analysis": {
                "engine_version": __version__,
                "game_rule_revision": "installed-1.6.15-audit-2026-11-02",
                "session_assumptions": (
                    "Without an explicit start, sequence predictions begin after each saved counter and calendar predictions begin on the saved day.",
                    "Future predictions hold saved flags, equipment and progression constant unless an explicit alternative states otherwise.",
                    "Each container column at an opening number is an alternative for that opening at Clint; opening earlier rows can change later flags and outcomes.",
                    "Mystery Boxes increment both GeodesCracked and MysteryBoxesOpened at Clint; their contents use the MysteryBoxesOpened sequence.",
                    "Each artifact spot is evaluated as the host player's next dig; digging one spot can change counters for the others.",
                    "Session RNG, online players and future actions are not reconstructed from the save; affected results are conditional or unavailable.",
                ),
                "rules_version": state.rules_version,
                "version_source": "saved"
                if state.metadata.game_version
                else "legacy_flags",
                "requested": {
                    "progress": PROGRESS_SECTIONS
                    if options.progress is None
                    else options.progress,
                    "predictions": tuple(REGISTRY)
                    if options.predictions is None
                    else options.predictions,
                    "extras": options.extras,
                    "bubbles": options.bubbles,
                    "artifacts": options.artifacts,
                    "locations": options.locations,
                },
                "prediction_settings": {
                    "start": settings.start,
                    "count": settings.count,
                    "day_offset": settings.day_offset,
                    "base_daily_luck": settings.daily_luck
                    if settings.daily_luck is not None
                    else -0.1,
                    "luck_policy": "explicit"
                    if settings.daily_luck is not None
                    else "conservative_lower_bound",
                    "luck_level": settings.luck_level,
                    "special_charm": "applied_per_player",
                    "player_indices": indices,
                    "game_start": settings.game_start,
                    "item_filter": settings.item_filter,
                },
                "artifact_daily_luck": state.metadata.daily_luck
                if options.artifacts
                else None,
                "prediction_coverage": coverage,
            },
        }
    )
