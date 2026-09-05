"""Command-line entry point. Diagnostic messages go to stderr only."""

from __future__ import annotations
import argparse
import sys
import time
from . import __version__
from .save import atomic_write, check_output_path, read_save


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="stardew-report",
        description="Generate a native Python Stardew Valley progress and RNG report.",
        epilog="Pass the full farmer_ID save or its folder, not SaveGameInfo. Use - for stdout.",
    )
    parser.add_argument(
        "save", help="Save file or save folder (XML or zlib compressed)"
    )
    parser.add_argument(
        "output", nargs="?", help="Output file; defaults to <save>-report.txt"
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_option",
        help="Output file (alternative to positional output)",
    )
    parser.add_argument(
        "--only",
        choices=("all", "checkup", "predictor", "extras"),
        default="all",
        help="Generate only the selected report category",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--profile", action="store_true", help="Print section timings to stderr"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show a traceback for internal errors"
    )
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)
    if args.output is not None and args.output_option is not None:
        parser.error(
            "Specify the output either positionally or with --output, not both."
        )
    started = time.perf_counter()
    try:
        save = read_save(args.save)
        load_seconds = time.perf_counter() - started
        extension = "json" if args.format == "json" else "txt"
        output = (
            args.output_option or args.output or f"{save.path.name}-report.{extension}"
        )
        destination = check_output_path(output, save.path) if output != "-" else None
        from .report import build_report

        report = build_report(save, args.only)
        content = report.json() if args.format == "json" else report.text()
        if destination is None:
            sys.stdout.write(content)
        else:
            atomic_write(destination, content)
            print(
                f"Wrote {output} ({len(content.encode('utf-8')) / 1024:.0f} KB)",
                file=sys.stderr,
            )
        if args.profile:
            timings = {
                "read": load_seconds,
                **report.timings,
                "total": time.perf_counter() - started,
            }
            print(
                "Timings: "
                + ", ".join(
                    f"{name}={seconds:.3f}s" for name, seconds in timings.items()
                ),
                file=sys.stderr,
            )
        return 0
    except BrokenPipeError:
        # Closing a pager early should not emit a traceback on interpreter exit.
        import os

        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        if args.debug:
            raise
        print(f"stardew-report: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
