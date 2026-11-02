from collections.abc import Mapping
from dataclasses import fields, is_dataclass

from stardew.domain.models.game_data import GameData
from stardew.domain.models.results import AnalysisResult

from .extras import render_extras


def clock(time):
    return f"{time // 100:02}:{time % 100:02}"


def heading(title):
    return f"\n{title}\n{'=' * len(title)}"


def metric_line(metric):
    mark = "[x]" if metric.complete else "[ ]"
    count = str(metric.count) if metric.count is not None else "unknown"
    goal = str(metric.goal) if metric.goal is not None else "unknown"
    percentage = f" ({metric.percentage:.2f}%)" if metric.percentage is not None else ""
    detail = []
    if not metric.possible:
        detail.append("unavailable")
    if metric.weight is not None:
        detail.append(f"contribution: {metric.earned:.2f}/{metric.weight:g}%")
    if metric.player_id is not None:
        detail.append(f"player: {metric.player_id}")
    return f"{mark} {metric.name}: {count}/{goal}{percentage}" + (
        " — " + "; ".join(detail) if detail else ""
    )


def fact_value(value):
    if isinstance(value, Mapping):
        return record_line(value)
    if is_dataclass(value):
        if hasattr(value, "name") and hasattr(value, "value"):
            return f"{value.name}: {fact_value(value.value)}"
        if all(hasattr(value, field) for field in ("year", "season", "day")):
            return f"{value.season} {value.day}, year {value.year}"
        return record_line(value)
    if isinstance(value, (tuple, list)):
        return ", ".join(fact_value(child) for child in value)
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def progress_item_line(item):
    detail = []
    if item.count is not None:
        detail.append(
            f"{item.count}/{item.goal}" if item.goal is not None else str(item.count)
        )
    if item.missing is not None and item.missing > 0:
        detail.append(f"missing: {item.missing}")
    for field in (
        "category",
        "quality",
        "cost",
        "cost_unit",
        "level",
        "next_goal",
        "next_missing",
        "hearts",
        "status",
        "kind",
        "event_ids",
    ):
        value = getattr(item, field, None)
        if value is not None and value != ():
            detail.append(f"{field.replace('_', ' ')}: {fact_value(value)}")
    if item.hint:
        detail.append(item.hint)
    if item.alternatives:
        detail.append("alternatives: " + fact_value(item.alternatives))
    return f"* {item.name} [{item.item_id}]" + (
        " — " + "; ".join(detail) if detail else ""
    )


def record_line(record):
    """Render the factual fields supplied by a prediction rule."""
    if is_dataclass(record):
        entries = [
            (field.name, getattr(record, field.name))
            for field in fields(record)
            if field.name != "snapshot"
        ]
    elif isinstance(record, Mapping):
        entries = record.items()
    else:
        return fact_value(record)
    return " | ".join(
        f"{key}: {fact_value(value)}"
        for key, value in entries
        if value is not None and value != ()
    )


def render_text(result: AnalysisResult, *, data: GameData) -> str:
    meta = result.metadata
    out = [
        "STARDEW VALLEY SAVE REPORT",
        f"Save file: {result.save_file}",
        f"Game: {meta.game_version or 'unknown'} | {meta.season or 'unknown'} {meta.day if meta.day is not None else '?'} | year {meta.year if meta.year is not None else '?'} | days played {meta.days_played if meta.days_played is not None else 'unknown'}",
    ]
    analysis = result.provenance.get("analysis", {})
    if analysis:
        out.append(heading("Analysis assumptions"))
        out.append(
            f"Engine: {analysis['engine_version']} | Rules: {analysis['rules_version']} ({analysis['version_source']})"
        )
        if analysis.get("game_rule_revision"):
            out.append(f"Game-rule revision: {analysis['game_rule_revision']}")
        out.extend(
            str(assumption) for assumption in analysis.get("session_assumptions", ())
        )
        if analysis["requested"]["predictions"]:
            settings = analysis["prediction_settings"]
            out.append(
                f"Prediction base luck: {settings['base_daily_luck']:g} ({settings['luck_policy'].replace('_', ' ')}); luck level: {settings['luck_level']}; special charm applied per player."
            )
            out.append(
                "Selected players (zero-based): "
                + ", ".join(map(str, settings["player_indices"]))
            )
        if analysis["requested"]["artifacts"]:
            out.append(
                f"Artifact base luck from save: {fact_value(analysis['artifact_daily_luck'])}. "
                "Effective luck includes Special Charm and the online-player average. "
                "Each spot is evaluated as the host's next dig; route order is not simulated."
            )
    for section in result.progress:
        out.append(heading(section.title))
        out.extend(metric_line(metric) for metric in section.metrics)
        out.extend(f"* {fact.name}: {fact_value(fact.value)}" for fact in section.facts)
        out.extend(progress_item_line(item) for item in section.items)
        for player in section.players:
            out.append(f"\nPlayer: {player.name}")
            out.extend(metric_line(metric) for metric in player.metrics)
            out.extend(
                f"* {fact.name}: {fact_value(fact.value)}" for fact in player.facts
            )
            out.extend(progress_item_line(item) for item in player.items)
        out.extend("! " + str(note) for note in section.diagnostics)
    for section in result.predictions:
        out.append(heading(section.title))
        if section.section_id in ("geode", "mystery"):
            out.append(
                "Sequence is the opening number, not an item ID. Each container at the same "
                "number is an alternative for that opening. openings_ahead: 1 means the next opening."
            )
            if section.section_id == "geode":
                out.append(
                    "Clint shares this counter across geodes, Artifact Troves, Golden Coconuts "
                    "and Mystery Boxes. Opening a Mystery Box also advances the geode sequence."
                )
            counters = {
                (record.player_id, fact.value)
                for record in section.records
                for fact in record.facts
                if fact.name == "saved_counter"
            }
            for player_id, counter in sorted(counters, key=lambda value: str(value[0])):
                out.append(
                    f"Player {player_id}: {counter} openings recorded in the save; "
                    f"next opening: #{counter + 1}."
                )
        coverage = analysis.get("prediction_coverage", {}).get(section.section_id)
        if coverage:
            if coverage["first_day"] is not None:
                out.append(
                    f"Days played: {coverage['first_day']}–{coverage['last_day']}"
                )
            if coverage["first_sequence"] is not None:
                out.append(
                    f"Sequence: {coverage['first_sequence']}–{coverage['last_sequence']}"
                )
        if section.available and not section.records:
            out.append("No results for the requested range and filters.")
        for record in getattr(section, "records", getattr(section, "entries", ())):
            out.append("* " + record_line(record))
        for note in getattr(section, "diagnostics", ()):
            out.append("! " + str(note))
    if result.bubbles or analysis.get("requested", {}).get("bubbles"):
        out.append(heading("Fishing bubbles"))
        if any(event.scenario for event in result.bubbles):
            out.append(
                "Conditional timelines: a frenzy attempt can select an ineligible fish using session RNG. "
                "Only events without a scenario occur in every forecast; the alternatives are not simultaneous."
            )
        if not result.bubbles:
            out.append("No results. Check diagnostics for unavailable features.")
        for event in result.bubbles:
            end = clock(event.end) if event.end is not None else ">25:50"
            out.append(
                f"{event.location:<18} ({event.x},{event.y}) {clock(event.start)}–{end} {event.kind}"
                + (f" [if {event.scenario}]" if event.scenario else "")
            )
    if result.artifacts or analysis.get("requested", {}).get("artifacts"):
        out.append(heading("Artifact spots"))
        if not result.artifacts:
            out.append("No results. Check diagnostics for unavailable features.")
        for spot in result.artifacts:
            loot = " + ".join(
                f"{item.quantity}× {item.name} [{item.item_id}]" for item in spot.items
            )
            out.append(
                f"{spot.location} ({spot.x},{spot.y}): {loot}"
                + (f" — {spot.note}" if spot.note else "")
            )
    if result.extras is not None:
        out.extend(
            [
                heading("Inventory and additional saved details"),
                render_extras(result.extras, data),
            ]
        )
    if result.diagnostics:
        out.append(heading("Diagnostics"))
        out.extend(
            f"! {diagnostic.feature}: {diagnostic.message}"
            for diagnostic in result.diagnostics
        )
    return "\n".join(out) + "\n"
