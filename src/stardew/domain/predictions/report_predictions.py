"""Structured analysis for the report's twenty-two prediction features."""

from collections.abc import Mapping, Sequence
from functools import partial
from typing import Any

from stardew.domain.errors import FeatureUnavailable
from stardew.domain.models.game_data import GameData
from stardew.domain.models.state import GameState

from . import report_rules as rules
from .inputs import _context_save, player_values
from .records import build_records, item_identities
from .records.common import RecordContext
from .registry import REGISTRY, SECTION_IDS, day_window
from .report_models import (
    PredictionSection,
    ReportPredictionOptions,
)
from .windows import CALENDAR_FEATURES, calculation_offset, calculation_offsets

PredictionOptions = ReportPredictionOptions


def _records(section, context, data, identities=None):
    """Compatibility adapter for historical captured-vector tests."""
    identities = item_identities(data) if identities is None else identities
    return [
        record
        for _, raw in context.captures
        for record in build_records(
            section, raw, RecordContext.from_prediction(context), identities
        )
    ]


def _append_records(records, section, context, identities, _feature, facts):
    records.extend(build_records(section, facts, context, identities))


def analyze_predictions(
    state: GameState,
    data: GameData,
    sections: Sequence[str] | None = None,
    options: ReportPredictionOptions | Mapping[str, Any] | None = None,
) -> tuple[PredictionSection, ...]:
    options = PredictionOptions() if options is None else options
    if isinstance(options, Mapping):
        options = PredictionOptions(**options)
    if not isinstance(options, PredictionOptions):
        raise TypeError("prediction options must be PredictionOptions or a mapping")
    selected = SECTION_IDS if sections is None else tuple(dict.fromkeys(sections))
    unknown = set(selected) - set(SECTION_IDS)
    if unknown:
        raise ValueError("Unknown prediction sections: " + ", ".join(sorted(unknown)))
    if not selected:
        return ()
    if options.player_indices is not None and any(
        i >= len(state.players) for i in options.player_indices
    ):
        raise ValueError("Prediction player index is outside the save player list.")
    save = _context_save(state, data, options)
    identities = item_identities(data)
    results = []
    for section in selected:
        spec = REGISTRY[section]
        diagnostics = []
        minimum = spec.minimum
        if minimum and rules.compare_version(save["version"], minimum) < 0:
            diagnostics.append(
                f"{spec.title} requires game version {minimum} or later."
            )
        if (
            spec.range_kind in ("days", "games")
            and options.start is None
            and save["daysPlayed"] is None
        ):
            diagnostics.append(
                "Save does not contain days_played; prediction dates cannot be calculated."
            )
        if section == "makeover" and len(save["characters"]) < 6:
            diagnostics.append(
                "Desert Festival vendor predictions require the saved NPC pool."
            )
        selected_players = (
            options.player_indices
            if options.player_indices is not None
            else tuple(range(len(state.players)))
        )
        players = selected_players if spec.scope == "player" else (0,)
        if (
            spec.player_id_since
            and rules.compare_version(save["version"], spec.player_id_since) >= 0
        ):
            missing = tuple(
                i for i in selected_players if state.players[i].player_id is None
            )
            if missing:
                diagnostics.append(
                    "Saved player ID required for deterministic seeds: "
                    + ", ".join(state.players[i].identity(i) for i in missing)
                )
        if diagnostics:
            if sections is not None and len(selected) == 1:
                raise FeatureUnavailable(diagnostics[0])
            results.append(
                PredictionSection(section, spec.title, (), tuple(diagnostics), False)
            )
            continue
        records = []
        window = day_window(spec, save["daysPlayed"], options.start, options.count)
        for player_index in players:
            for offset in calculation_offsets(spec, save, options, player_index):
                working = dict(save)
                if spec.scope == "player":
                    working.update(player_values(state, options, player_index))
                working["_calculation_offset"] = calculation_offset(
                    spec, working["daysPlayed"], offset
                )
                context = rules.PredictionContext(
                    working, data.catalogs, player_index, options.count
                )
                context.selected_players = selected_players
                context.player_scoped = spec.scope == "player"
                context.record_sink = partial(
                    _append_records,
                    records,
                    section,
                    RecordContext.from_prediction(context),
                    identities,
                )
                if window is not None and section in CALENDAR_FEATURES:
                    context.day_range = (window.start, window.stop)
                if section == "cj":
                    spec.calculate(context, False, offset, options.game_start - 1)
                else:
                    spec.calculate(context, False, offset)
        if window is not None:
            records = [
                record
                for record in records
                if record.date and window.contains(record.date.days_played)
            ]
        elif (
            section == "makeover"
            and options.start is None
            and save["daysPlayed"] is not None
        ):
            records = [
                record
                for record in records
                if record.date is None or record.date.days_played >= save["daysPlayed"]
            ]
        if options.item_filter:
            query = options.item_filter.casefold()
            records = [
                record
                for record in records
                if query in (record.item_name or "").casefold()
                or query in (record.item_id or "").casefold()
                or any(query in str(fact.value).casefold() for fact in record.facts)
            ]
        results.append(
            PredictionSection(section, spec.title, tuple(records), tuple(diagnostics))
        )
    return tuple(results)


__all__ = ["PredictionOptions", "SECTION_IDS", "analyze_predictions"]
