"""One command for reports, isolated predictions, exports and PNG maps."""

from __future__ import annotations
import argparse
import sys
import time

from stardew import __version__
from stardew.api import load_save, load_game_data, analyze, AnalysisOptions
from stardew.domain.errors import FeatureUnavailable
from stardew.infrastructure.saves import SaveError, atomic_write, check_output_path
from stardew.infrastructure.game_data import DataError
from stardew.presentation.json import render_json
from stardew.presentation.text import render_text


def parser():
    root = argparse.ArgumentParser(
        prog="stardew",
        description="Analyze saved progress and deterministic predictions.",
    )
    root.add_argument("--version", action="version", version=__version__)
    root.add_argument("--debug", action="store_true", help="show internal tracebacks")
    commands = root.add_subparsers(dest="command", required=True)
    report = commands.add_parser(
        "report", help="generate a complete or selected report"
    )
    report.add_argument("save")
    report.add_argument(
        "--only", choices=("all", "progress", "predictions", "extras"), default="all"
    )
    report.add_argument(
        "--section",
        action="append",
        help="select a progress or prediction section; repeat to select several",
    )
    report.add_argument("--profile", action="store_true")
    predict = commands.add_parser("predict", help="run one prediction feature")
    predict.add_argument(
        "feature", help="bubbles, artifacts, or a report prediction ID"
    )
    predict.add_argument("save")
    for command in (report, predict):
        command.add_argument("--format", choices=("text", "json"), default="text")
        command.add_argument(
            "-o", "--output", default="-", help="destination; default stdout"
        )
        command.add_argument(
            "--data-dir", help="directory of exported 1.6.15 game tables"
        )
        command.add_argument(
            "--location",
            action="append",
            help="location filter; repeat for several maps",
        )
        command.add_argument("--resources", help="external JSON/RESX map geometry")
        command.add_argument(
            "--plot", help="write annotated PNG maps to this directory"
        )
        command.add_argument(
            "--game-dir", help="installed game directory for PNG backgrounds"
        )
        command.add_argument(
            "--start",
            type=int,
            help="first day or sequence index for report predictions",
        )
        command.add_argument(
            "--count", type=int, help="number of days or sequence entries"
        )
    data = commands.add_parser("data", help="export local game tables")
    data_commands = data.add_subparsers(dest="data_command", required=True)
    export = data_commands.add_parser("export")
    export.add_argument("game")
    export.add_argument("--output", required=True)
    return root


def options_for(args):
    locations = tuple(args.location) if args.location else None
    prediction_options = None
    if args.start is not None or args.count is not None:
        from stardew.domain.predictions.report_predictions import PredictionOptions

        prediction_options = PredictionOptions(start=args.start, count=args.count)
    if args.command == "predict":
        return AnalysisOptions(
            progress=(),
            predictions=()
            if args.feature in ("bubbles", "artifacts")
            else (args.feature,),
            extras=False,
            bubbles=args.feature == "bubbles",
            artifacts=args.feature == "artifacts",
            locations=locations,
            prediction_options=prediction_options,
            strict=True,
        )
    progress = None if args.only in ("all", "progress") else ()
    predictions = None if args.only in ("all", "predictions") else ()
    if args.section:
        from stardew.domain.progress import PROGRESS_SECTIONS as SECTION_IDS
        from stardew.domain.predictions.report_predictions import (
            SECTION_IDS as PREDICTION_IDS,
        )

        unknown = set(args.section) - set(SECTION_IDS) - set(PREDICTION_IDS)
        if unknown:
            raise ValueError("Unknown report section: " + ", ".join(sorted(unknown)))
        progress = tuple(section for section in args.section if section in SECTION_IDS)
        predictions = tuple(
            section for section in args.section if section in PREDICTION_IDS
        )
    return AnalysisOptions(
        progress=progress,
        predictions=predictions,
        extras=args.only in ("all", "extras") and not args.section,
        bubbles=args.only == "all" and not args.section,
        artifacts=args.only == "all" and not args.section,
        locations=locations,
        prediction_options=prediction_options,
    )


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        started = time.perf_counter()
        if args.command == "data":
            from stardew.infrastructure.xnb.exporter import export_game_data

            export_game_data(args.game, args.output)
            print(f"Exported game tables to {args.output}")
            return 0
        if bool(args.plot) != bool(args.game_dir):
            raise ValueError("--plot and --game-dir must be supplied together.")
        state = load_save(args.save)
        output = (
            check_output_path(args.output, state.source) if args.output != "-" else None
        )
        data = load_game_data(args.data_dir, resources=args.resources)
        result = analyze(state, data=data, options=options_for(args))
        if args.plot:
            from stardew.presentation.maps import save_plots

            for mode, events in (
                ("bubbles", result.bubbles),
                ("artifacts", result.artifacts),
            ):
                if events:
                    for path in save_plots(
                        state, events, args.plot, args.game_dir, mode
                    ):
                        print(f"Saved figure: {path}", file=sys.stderr)
        content = (
            render_json(result)
            if args.format == "json"
            else render_text(result, data=data)
        )
        if output is None:
            sys.stdout.write(content)
        else:
            atomic_write(output, content)
            print(f"Wrote {output}", file=sys.stderr)
        if getattr(args, "profile", False):
            print(f"Elapsed: {time.perf_counter() - started:.3f}s", file=sys.stderr)
        return 0
    except (SaveError, DataError, FeatureUnavailable, OSError, ValueError) as error:
        if args.debug:
            raise
        print(f"Error: {error}", file=sys.stderr)
        return 1
