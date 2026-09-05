# stardew-report

Generate Stardew Valley progress and prediction reports with **native Python**.
No Node.js, JavaScript engine, jsdom, or browser is needed at runtime.

Reports cover achievements, skills, friendships, recipes, fishing, shipping,
the museum, bundles, walnuts, and perfection, plus all prediction tabs from
the original script: mines, geodes, mystery boxes, merchants, night events,
books, enchantments, Calico Jack, and more. Reports use the upstream projects'
English text and contain spoilers.

## Installation and usage

Requires Python 3.11 or later. From the project directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/stardew-report /path/to/Farmer_123456789
```

With uv, install the dependencies pinned in `uv.lock` and run the application:

```sh
uv run --locked stardew-report /path/to/Farmer_123456789
```

Once the dependencies are installed, you can also run directly from a checkout:

```sh
python3 stardew-report.py /path/to/Farmer_123456789
python3 -m stardew_report /path/to/Farmer_123456789 my-report.txt
python3 stardew-report.py /path/to/Farmer_123456789 - | less
python3 stardew-report.py /path/to/Farmer_123456789 --format json -o report.json
python3 stardew-report.py /path/to/Farmer_123456789 --only checkup --profile
```

The input can be the full `farmer_ID` save file or its containing folder.
`SaveGameInfo` contains only a summary and is rejected. XML, XML with a byte
order mark (BOM), and zlib-compressed saves are detected by their contents,
including small files.

By default, the report is written to `<save>-report.txt` in the current
directory, or `<save>-report.json` with `--format json`. Use `-` to send only
the report to stdout; diagnostics and `--profile` output go to stderr.
`--only` accepts `all`, `checkup`, `predictor`, or `extras`. JSON output includes
metadata, text sections, and execution timings, with `schema_version: 1`.

Reading a save never modifies it. Reports are written to a temporary file and
replaced atomically. Attempts to overwrite the input save, including through
a hard link, are rejected. Input errors produce concise messages; `--debug`
shows tracebacks for investigating internal failures.

## Changes from the JavaScript version

- XML is parsed once, using compiled and cached lxml queries.
- Calculation rules are ported to Python functions, with data tables in JSON.
- The `System.Random` generator and xxHash32 hashes use Python APIs while
  preserving signed arithmetic, overflow behavior, and 64-bit player IDs.
- The old `TextEncoder` adapter created buffers outside the jsdom context,
  causing the hash library to interpret them incorrectly. Different strings
  could produce the same hash. The Python implementation avoids this issue.
- Seed preparation preserves large player IDs. The original helper modified
  `arguments`, which does not update named parameters in strict mode, allowing
  IDs to be rounded during subsequent numeric conversion.
- Extra details are read directly from XML. Shipping quantities include fish
  and other items previously filtered out by the shipping achievement list.
  Unknown item IDs appear as `#ID`.
- A single animal in a single building appears in the extra details without
  relying on an intermediate parser to represent single elements as arrays.

The seed fixes can change predictions compared with the old report. During
the migration, results were compared with the reference engines after applying
these two explicit corrections. The JavaScript sources and temporary
comparison tools were removed after validation.

## Validation and measured performance

Local measurements with a test save, using `/usr/bin/time`:

| Implementation | Total time | Peak RSS memory |
| --- | ---: | ---: |
| Original JavaScript wrapper | 10.13 s | 778 MiB |
| Python, final run | 3.07 s | 80 MiB |

These are individual local runs, not a universal benchmark. All 27 Checkup
sections and 22 Predictor tabs matched the corrected reference on a test save,
its backup, and five variants: compression, BOM, Unicode, multiplayer, and
legacy randomness. The 15 unit tests passed on Python 3.13 and 3.14. A wheel
installation was also run outside the repository with an empty `PATH`, without
access to Node.js or the original JavaScript sources.

## Project structure and maintenance

| Location | Responsibility |
| --- | --- |
| `stardew_report/save.py` | Save loading, validation, and atomic output |
| `stardew_report/report.py` | Report assembly and section selection |
| `stardew_report/extras.py` | XP, shipping, rarecrows, animals, and waivers |
| `stardew_report/rng.py` | Game randomness and deterministic hashes |
| `stardew_report/query.py` | XML queries and default control values |
| `stardew_report/formatting.py` | Markup-to-text conversion |
| `stardew_report/engines/` | Calculation engines ported to Python |
| `stardew_report/data/` | Tables, script-free templates, and license notices |
| `stardew_report/runtime.py` | Explicit value semantics used by the rules |

The engines and tables are required application code and data. The rules are
static Python: no JavaScript interpreter, `eval`, or runtime translation is
used. The value layer preserves relevant differences between the languages,
such as arrays also used as maps and numeric property ordering. Queries use
lxml trees without running scripts, rendering pages, or fetching external
resources. HTML5 parsing preserves table and list formatting.

Update calculation rules in the Python modules and add tests for affected
behavior. Update data in the JSON files. Engine comments record upstream
source line numbers for reference.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Tests cover RNG and hash vectors obtained from the reference sources, player
ID precision, XML queries, invalid input, and write failures. These vectors
are maintained test fixtures, not disposable reports. Personal saves are not
included in the test suite.

The upstream compatibility branches have been preserved, but changes should
be validated against saves from the corresponding game versions.

## License and credits

This project is licensed under the MIT License, copyright 2026 lsiddd. See
[LICENSE](LICENSE). Derived components retain their respective authors'
notices, collected in [LICENSES.txt](stardew_report/data/LICENSES.txt).

Rules and data are derived from
[Stardew Checkup](https://github.com/MouseyPounds/stardew-checkup) and
[Stardew Predictor](https://github.com/MouseyPounds/stardew-predictor), by
MouseyPounds, and [stardew.app](https://github.com/communitycenter/stardew.app),
by the Community Center team.

Upstream commits used for the migration:

- Checkup: `8e48aa1`.
- Predictor: `b9e7c71`.
- stardew.app: `7b27120`.
