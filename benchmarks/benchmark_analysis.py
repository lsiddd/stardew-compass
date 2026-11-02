"""Measure loaded analysis, cold CLI, serialization and optional peak memory."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tracemalloc
from collections.abc import Callable
from pathlib import Path
from statistics import median
from tempfile import TemporaryDirectory
from time import perf_counter

from stardew.api import (
    AnalysisOptions,
    ReportPredictionOptions,
    analyze,
    load_game_data,
    load_save,
)
from stardew.domain.predictions.report_predictions import analyze_predictions
from stardew.domain.progress import analyze_progress
from stardew.presentation.json import render_json
from stardew.presentation.text import render_text


def median_ms(calculate: Callable[[], object], repeat: int) -> float:
    calculate()
    durations = []
    for _ in range(repeat):
        started = perf_counter()
        calculate()
        durations.append((perf_counter() - started) * 1000)
    return round(median(durations), 3)


def synthetic_save(data, objects: int) -> str:
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
    placed = "".join(
        f"<item><key><Vector2><X>{index % 100}</X><Y>{index // 100}</Y></Vector2></key><value><Object><itemId>388</itemId><name>Wood</name><Stack>1</Stack></Object></value></item>"
        for index in range(objects)
    )
    return f"""<SaveGame><uniqueIDForThisGame>123456789</uniqueIDForThisGame>
<gameVersion>1.6.15</gameVersion><year>2</year><dayOfMonth>16</dayOfMonth><currentSeason>summer</currentSeason><dailyLuck>0.1</dailyLuck>
<player><name>Farmer</name><gender>Female</gender><UniqueMultiplayerID>123456789012345678</UniqueMultiplayerID>
<stats><Values>{stats}</Values></stats><deepestMineLevel>120</deepestMineLevel>
<mailReceived><string>ccCraftsRoom</string><string>ccVault</string><string>ccPantry</string></mailReceived></player>
<locations><GameLocation><name>Town</name><characters>{npcs}</characters><objects>{placed}</objects></GameLocation></locations></SaveGame>"""


def measure(path, data, args):
    state = load_save(path)
    options = AnalysisOptions(bubbles=bool(args.save), artifacts=bool(args.data_dir))
    report = analyze(state, data=data, options=options)
    timings = {
        "load_save_ms": median_ms(lambda: load_save(path), args.repeat),
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
        "report_text_ms": median_ms(
            lambda: render_text(report, data=data), args.repeat
        ),
        "report_json_ms": median_ms(lambda: render_json(report), args.repeat),
    }
    result = {
        "repeat": args.repeat,
        "save_bytes": path.stat().st_size,
        "save_nodes": sum(1 for _ in state.snapshot.iter()),
        "median_ms": timings,
    }
    if args.cold:
        command = [
            sys.executable,
            "-I",
            "-m",
            "stardew",
            "report",
            str(path),
            "--format",
            "json",
        ]
        if args.data_dir:
            command.extend(("--data-dir", str(args.data_dir)))
        result["cold_cli_ms"] = median_ms(
            lambda: subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True
            ),
            args.repeat,
        )
    if args.memory:
        tracemalloc.start()
        loaded = load_save(path)
        calculated = analyze(loaded, data=data, options=options)
        render_json(calculated)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        result["load_analysis_json_peak_mib"] = round(peak / 1024**2, 3)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument(
        "--save", type=Path, help="Optional local save; contents are never printed"
    )
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument(
        "--objects", type=int, default=0, help="Number of synthetic placed objects"
    )
    parser.add_argument(
        "--cold",
        action="store_true",
        help="Measure a fresh CLI process including imports and output",
    )
    parser.add_argument(
        "--memory",
        action="store_true",
        help="Measure Python allocations separately from timings",
    )
    args = parser.parse_args()
    if args.repeat < 1 or args.objects < 0:
        parser.error("repeat must be positive and objects nonnegative")
    if args.save and args.objects:
        parser.error("--objects applies only to the synthetic save")
    data = load_game_data(args.data_dir)
    with TemporaryDirectory(prefix="stardew-benchmark-") as folder:
        path = args.save.resolve() if args.save else Path(folder) / "Farmer_123456789"
        if not args.save:
            path.write_text(synthetic_save(data, args.objects), encoding="utf-8")
        result = measure(path, data, args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
