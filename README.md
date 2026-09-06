# stardew-report

Generate a readable report from a Stardew Valley save: track progress, find
missing collectibles, inspect stored items, and preview random events.

The command-line tool runs locally in Python and exports plain text or JSON.
Reports are in English and contain spoilers.

## What the report includes

| Category | Contents |
| --- | --- |
| `checkup` | Achievements, money, skills, quests, friendships, recipes, fishing, shipping, museum donations, bundles, walnuts, perfection, and more |
| `predictor` | Predictions for mines, geodes, mystery boxes, merchants, night events, books, enchantments, Calico Jack, and more |
| `extras` | Player inventories, chest and fridge contents, equipment, tool attachments, skill XP, shipping quantities, rarecrows, animal details, and perfection waivers |

Inventory lists show each item's slot, name, quantity, quality, and ID. Chests
are listed separately, with their location, tile coordinates when saved, and
custom Chests Anywhere name when available. Storage inside buildings is
included, and empty containers are marked explicitly. Items without a known
name use their ID as a fallback.

## Installation

Requires **Python 3.11 or later**. Run the following commands from the project
directory.

With **uv**, run the tool using the dependencies pinned in `uv.lock`:

```sh
uv run --locked stardew-report /path/to/Farmer_123456789
```

With **pip**, install into a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
stardew-report /path/to/Farmer_123456789
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in
PowerShell instead of the `source` command.

## Usage

Pass the full save file, usually named `<farmer>_<ID>`, or the folder containing
that file. `SaveGameInfo` is only a summary and cannot be used to generate a
report. The loader detects XML, XML with a byte order mark (BOM), and
zlib-compressed saves automatically.

The examples below use the installed command. With uv, prefix each command
with `uv run --locked`.

```sh
# Generate the complete report.
stardew-report /path/to/Farmer_123456789

# Choose the output path.
stardew-report /path/to/Farmer_123456789 -o my-report.txt

# Export as JSON.
stardew-report /path/to/Farmer_123456789 --format json -o report.json

# List inventories, chests, and the other extra details.
stardew-report /path/to/Farmer_123456789 --only extras

# Read a progress report in a terminal pager.
stardew-report /path/to/Farmer_123456789 - --only checkup | less

# Generate predictions and print execution timings.
stardew-report /path/to/Farmer_123456789 --only predictor --profile
```

By default, output goes to `<save>-report.txt` in the current directory, or
`<save>-report.json` when using `--format json`. An output path can also be
passed as the second positional argument. Use `-` to write the report to
stdout; diagnostics and timings go to stderr.

| Option | Description |
| --- | --- |
| `--only all\|checkup\|predictor\|extras` | Select a report category; defaults to `all` |
| `--format text\|json` | Select the output format; defaults to `text` |
| `-o PATH`, `--output PATH` | Set the output destination |
| `--profile` | Print execution timings to stderr |
| `--debug` | Show tracebacks when an error occurs |
| `--version` | Print the generator version |
| `--help` | Show all command-line options |

JSON output contains save metadata, a summary, report sections, and execution
timings, with `schema_version: 1`. Each section includes a title, category, and
text body; inventory lists are part of the `extras` text body.

The save is read without modification. Reports are written atomically, and
output paths that would overwrite the input save are rejected.

## Development

Once dependencies are installed, run the source directly with either entry
point:

```sh
python3 -m stardew_report /path/to/Farmer_123456789
python3 stardew-report.py /path/to/Farmer_123456789
```

The save is parsed once with lxml. Python modules implement the progress and
prediction rules using bundled JSON data. Randomness calculations preserve
signed arithmetic, overflow behavior, and 64-bit player IDs. HTML templates
are used to assemble report text. Report generation does not require network
access or a browser.

| Location | Responsibility |
| --- | --- |
| `stardew_report/cli.py` | Command-line options and diagnostics |
| `stardew_report/save.py` | Save loading, validation, and atomic output |
| `stardew_report/report.py` | Report assembly and category selection |
| `stardew_report/inventory.py` | Player inventories, equipment, and chest contents |
| `stardew_report/extras.py` | XP, shipping, rarecrows, animals, and waivers |
| `stardew_report/engines/` | Progress and prediction rules |
| `stardew_report/rng.py` | Game randomness and deterministic hashes |
| `stardew_report/query.py` | XML queries and report template controls |
| `stardew_report/formatting.py` | HTML-to-text conversion |
| `stardew_report/runtime.py` | Value and arithmetic semantics used by the rules |
| `stardew_report/data/` | Data tables, templates, and license notices |
| `tests/` | Unit tests and synthetic fixtures |

Run the test suite from the project directory:

```sh
uv run --locked python -m unittest discover -s tests -v
```

With dependencies already installed, use
`python3 -m unittest discover -s tests -v`.

Tests cover RNG and hash vectors, player ID precision, XML queries, save
validation, write failures, inventory and chest parsing, and CLI output.
Personal saves are not included. When changing calculation rules or save
parsing, add regression tests and validate against saves from the affected
game versions.

## License and credits

Licensed under the MIT License, copyright 2026 lsiddd. See [LICENSE](LICENSE).
Derived components retain their authors' notices in
[LICENSES.txt](stardew_report/data/LICENSES.txt).

Rules and data are derived from these projects:

| Project | Authors | Source revision |
| --- | --- | --- |
| [Stardew Checkup](https://github.com/MouseyPounds/stardew-checkup) | MouseyPounds | `8e48aa1` |
| [Stardew Predictor](https://github.com/MouseyPounds/stardew-predictor) | MouseyPounds | `b9e7c71` |
| [stardew.app](https://github.com/communitycenter/stardew.app) | Community Center team | `7b27120` |
