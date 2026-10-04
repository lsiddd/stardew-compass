"""Measure warm analysis on a synthetic save without personal or local game data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median
from tempfile import TemporaryDirectory
from time import perf_counter
from collections.abc import Callable

from stardew.api import AnalysisOptions, analyze, load_game_data, load_save
from stardew.domain.predictions.report_predictions import analyze_predictions
from stardew.api import ReportPredictionOptions
from stardew.domain.progress import analyze_progress
from stardew.presentation.json import render_json


def median_ms(calculate: Callable[[], object], repeat: int) -> float:
    calculate()  # Warm module imports and caches before timing.
    durations = []
    for _ in range(repeat):
        started = perf_counter()
        calculate()
        durations.append((perf_counter() - started) * 1000)
    return round(median(durations), 3)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeat", type=int, default=5)
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be positive")
    data = load_game_data()
    stats = "".join(
        f"<item><key><string>{name}</string></key><value><unsignedInt>{value}</unsignedInt></value></item>"
        for name, value in (
            ("daysPlayed", 156),
            ("geodesCracked", 442),
            ("MysteryBoxesOpened", 10),
            ("timesEnchanted", 2),
            ("ticketPrizesClaimed", 5),
            ("trashCansChecked", 100),
        )
    )
    npcs = "".join(
        f"<NPC><name>{name}</name></NPC>"
        for name in data.catalogs["predictor_characters"]
    )
    xml = f"""<SaveGame><uniqueIDForThisGame>123456789</uniqueIDForThisGame>
      <gameVersion>1.6.15</gameVersion><year>2</year><dayOfMonth>16</dayOfMonth>
      <currentSeason>summer</currentSeason><dailyLuck>0.1</dailyLuck>
      <player><name>Farmer</name><gender>Female</gender>
      <UniqueMultiplayerID>123456789012345678</UniqueMultiplayerID>
      <stats><Values>{stats}</Values></stats><deepestMineLevel>120</deepestMineLevel>
      <mailReceived><string>ccCraftsRoom</string><string>ccVault</string>
      <string>ccPantry</string></mailReceived></player>
      <locations><GameLocation><name>Town</name><characters>{npcs}</characters>
      </GameLocation></locations></SaveGame>"""
    with TemporaryDirectory(prefix="stardew-benchmark-") as folder:
        path = Path(folder) / "Farmer_123456789"
        path.write_text(xml, encoding="utf-8")
        state = load_save(path)
        options = AnalysisOptions(bubbles=False, artifacts=False)
        report = analyze(state, data=data, options=options)
        timings = {
            "summary_ms": median_ms(
                lambda: analyze_progress(state, data, ("summary",)), args.repeat
            ),
            "mines_one_day_ms": median_ms(
                lambda: analyze_predictions(
                    state, data, ("mines",), ReportPredictionOptions(start=1, count=1)
                ),
                args.repeat,
            ),
            "mines_28_days_ms": median_ms(
                lambda: analyze_predictions(
                    state, data, ("mines",), ReportPredictionOptions(start=1, count=28)
                ),
                args.repeat,
            ),
            "report_analysis_ms": median_ms(
                lambda: analyze(state, data=data, options=options), args.repeat
            ),
            "report_json_ms": median_ms(lambda: render_json(report), args.repeat),
        }
    print(json.dumps({"repeat": args.repeat, "median_ms": timings}, indent=2))


if __name__ == "__main__":
    main()
