# Stardew Compass

**Know what's left to complete. Plan what comes next.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Turn your Stardew Valley save into a completion checklist, a calendar of
predictions, and annotated maps of fishing bubbles and artifact spots.
Stardew Compass brings progress tracking, inventories, and deterministic predictions
together in a local Python toolkit, with a command-line interface and a typed
API that share the same results.

Find the recipes you still need to cook, inspect your next geodes, look ahead
at the Traveling Cart, or check when fishing bubbles appear in the Mountain.
Read a text report, export structured JSON for your own tools, or generate PNG
maps using graphics from your game installation.

[Quick start](#quick-start) · [Reports](#understand-your-farm) ·
[Predictions](#plan-your-next-move) · [Maps](#fishing-bubbles-and-png-maps) ·
[Python API](#python-api) · [Development](#development)

## What you can do

| Task | What you get |
| --- | --- |
| Track completion | **27 progress sections** covering recipes, collections, relationships, quests, Ginger Island, and perfection. |
| Look ahead | **22 prediction features** covering shops, loot sequences, mine floors, events, enchantments, and more. |
| Find fishing opportunities | Bubble and frenzy locations, tile coordinates, and active time windows. |
| Inspect artifact spots | Predicted drops for saved spots, including quantities and conditional alternatives. |
| Explore your save | Player inventories, equipment, stored items, shared inventories, shipping records, and animals. |
| Build on the results | Immutable Python models and **JSON schema v2**, shared by the API and CLI. |

Save files and game assets are read locally. Reports are written to stdout or
to a destination you choose; the input save is protected from being overwritten.

> Reports and predictions reveal game content, event outcomes, and hidden
> progression details. Expect spoilers.

## Quick start

### Install with uv

Requires **Python 3.11 or later** and `uv`.

```sh
git clone https://github.com/lsiddd/stardew-compass.git
cd stardew-compass
uv sync --locked
```

Generate your first report:

```sh
uv run --locked stardew report "/path/to/Farmer_123"
```

Replace `/path/to/Farmer_123` with your full save file or its containing save
directory. The full file normally shares the directory's name, such as
`Farmer_123/Farmer_123`. `SaveGameInfo` contains only a summary; use the full
save for analysis.

The loader detects XML, UTF-8 BOM, UTF-16, and zlib-compressed saves
automatically. Paths containing spaces work when quoted.

### Install with pip

From the repository checkout, install into a Python 3.11+ environment:

```sh
python -m pip install .
stardew report "/path/to/Farmer_123"
```

The examples below use `uv run --locked stardew`. With a pip installation,
use `stardew` directly. `python -m stardew` is also available.

## Understand your farm

A complete report combines progress, report predictions, inventories, fishing
bubbles, and artifact spots. It keeps available results and includes diagnostics
for features that need a different game version or additional data.

### Choose the level of detail

```sh
uv run --locked stardew report "/path/to/Farmer_123"
uv run --locked stardew report "/path/to/Farmer_123" --only progress
uv run --locked stardew report "/path/to/Farmer_123" --only predictions
uv run --locked stardew report "/path/to/Farmer_123" --only extras
```

For a focused checklist, repeat `--section` with the sections you want:

```sh
uv run --locked stardew report "/path/to/Farmer_123" \
  --section cooking \
  --section crafting \
  --section perfection_tracker
```

Section selection returns only the selected progress and report predictions.
The perfection tracker calculates its contributing categories automatically,
including the best qualifying player for each category in multiplayer saves.

### Progress sections

Progress results include completion counts, goals, percentages, missing items,
and player-specific facts where applicable.

| Area | Section IDs |
| --- | --- |
| Farm overview | `summary`, `money`, `family`, `animals` |
| Player progression | `skills`, `skill_mastery`, `stardrops`, `powers` |
| Quests and relationships | `quests`, `special_orders`, `social`, `raccoons` |
| Recipes and collections | `cooking`, `crafting`, `fishing`, `basic_shipping`, `crop_shipping`, `museum` |
| Exploration and discoveries | `monsters`, `secret_notes`, `journal_scraps`, `walnuts`, `island_upgrades` |
| Completion milestones | `bundles`, `grandpa`, `perfection_tracker`, `arcade_games` |

### Inventories and extras

`--only extras` gathers each player's inventory and equipment, experience and
skill values, shipped items, containers, shared inventories, rarecrows,
animals, and saved perfection waivers. This is useful when you want to inspect
what a farm owns alongside its completion records.

### Save a report

```sh
uv run --locked stardew report "/path/to/Farmer_123" -o outputs/report.txt
uv run --locked stardew report "/path/to/Farmer_123" \
  --format json -o outputs/report.json
```

Text is the default format. `--format json` exports structured facts with
`snake_case` field names and `schema_version: 2`. File output is replaced
atomically; status messages go to stderr so stdout remains suitable for pipes.

## Plan your next move

Run one feature with `stardew predict FEATURE SAVE`. Predictions use the saved
game seed, version, counters, and player state, preserving the random-number
behavior expected by the corresponding rules.

### Available prediction features

| Feature | Command ID |
| --- | --- |
| Mine floor patterns | `mines` |
| Traveling Cart | `cart` |
| Geode contents | `geode` |
| Mystery Box contents | `mystery` |
| Train arrivals | `train` |
| Night events | `night` |
| Crane game | `crane` |
| Krobus's shop | `krobus` |
| Sandy's shop | `sandy` |
| Wallpaper and flooring | `wallpaper` |
| Garbage cans | `trash` |
| Tool and weapon enchantments | `enchant` |
| Mine chests | `minechest` |
| Gem Birds | `gembirds` |
| Feast of the Winter Star | `winterstar` |
| Desert Festival | `makeover` |
| Weather and green rain | `greenrain` |
| Calico Jack | `cj` |
| Bookseller | `book` |
| Statue blessings | `statue` |
| Prize tickets | `prize` |
| Raccoon requests and rewards | `raccoon` |

These IDs also work with `report --section`. Fishing bubbles and artifact spots
have their own prediction commands: `bubbles` and `artifacts`.

### Choose a prediction range

Inspect the next 20 geodes from the saved counter:

```sh
uv run --locked stardew predict geode "/path/to/Farmer_123" --count 20
```

Inspect a specific part of the geode sequence:

```sh
uv run --locked stardew predict geode "/path/to/Farmer_123" \
  --start 1 --count 20 --format json
```

Calculate mine patterns for the first three days of Year 2:

```sh
uv run --locked stardew predict mines "/path/to/Farmer_123" \
  --start 113 --count 3
```

The meaning of a range depends on the feature:

| Prediction type | Meaning of `--start` and `--count` |
| --- | --- |
| Calendar predictions, including mines, shops, trains, and Bookseller | First **day played** and number of days. Day 1 is Spring 1, Year 1; day 113 is Spring 1, Year 2. |
| Geodes, Mystery Boxes, enchantments, prize tickets, and raccoon requests | First **sequence index** and number of entries. Indices start at 1; `--count` alone continues from the saved counter. |
| Winter Star and Desert Festival | First **year** and number of years. |

Range options apply to report predictions. Bubble and artifact predictions use
the saved day. Feature availability follows the save's version and required
fields; an isolated prediction returns an error when its requirements are missing.

Conditional outcomes appear as explicit alternatives, with the condition that
selects each one. Session-dependent outcomes retain those alternatives when
the relevant random state is absent from the save.

## Fishing bubbles and PNG maps

Find bubble and frenzy events for the saved day:

```sh
uv run --locked stardew predict bubbles "/path/to/Farmer_123" \
  --location Mountain --location Beach
```

Bubble predictions support **Stardew Valley 1.6.9–1.6.x**. Default locations
are Town, Mountain, Forest, Beach, Desert, Woods, IslandNorth, IslandWest,
and IslandSouthEast. Riverland saves also include `Farm_Fishing`.

Bundled geometry supplies the tile data used by predictions. To use alternate
geometry, pass `--resources /path/to/maps.json` or a compatible `.resx` file.

### Generate annotated maps

Install the optional Pillow dependency:

```sh
uv sync --locked --extra plot
```

Generate PNGs using the backgrounds from your local game installation:

```sh
uv run --locked --extra plot stardew predict bubbles "/path/to/Farmer_123" \
  --location Mountain \
  --plot outputs/maps \
  --game-dir "/path/to/StardewValley"
```

For a pip installation, add plotting support with
`python -m pip install '.[plot]'` from the checkout. Supply `--plot` and
`--game-dir` together. Both `report` and `predict` can generate maps for their
bubble and artifact results.

### Read the map results

- Tile coordinates start at **zero**.
- Times use the game's clock notation: `610` is 06:10 and `2550` is 25:50.
- Bubble end times are exclusive. `end: null` means the event is still active
  at 25:50, the last simulated time.
- Backgrounds show the static game map. Saved buildings, crops, and changes
  made during a play session are outside the rendered background.
- Location results include island and festival maps independently of access
  restrictions. Artifact spots are evaluated individually.

## Artifact spots and local game data

Artifact predictions use the saved spots, the carried hoe and its enchantments,
and tables exported from the local game installation.

| Requirement | Expected value |
| --- | --- |
| Saved game version | **1.6.15** |
| Player inventory | **Exactly one hoe** |
| Game tables | `Objects.json`, `Locations.json`, and `ObjectNames.json` |
| Source information | `provenance.json` containing source hashes |

Export once to a directory outside the game installation:

```sh
uv run --locked stardew data export "/path/to/StardewValley" \
  --output outputs/game-data
```

Use the exported tables for a prediction or a complete report:

```sh
uv run --locked stardew predict artifacts "/path/to/Farmer_123" \
  --data-dir outputs/game-data

uv run --locked stardew report "/path/to/Farmer_123" \
  --data-dir outputs/game-data
```

The exporter reads XNB v5 tables, including LZX-compressed data, and records
SHA-256 hashes of the source files. The current object-name export reads
`Content/Strings/Objects.pt-BR.xnb`; artifact item names follow that table.
The game DLL is read as bytes for hashing.

Game tables and artwork stay in your local directories. PNG backgrounds are
read from the installation when plotting is requested. Secret-note drops that
depend on session RNG include explicit note-or-stone alternatives.

## Python API

Load a save once, choose the calculations you need, and reuse the resulting
models across text, JSON, and your own application code:

```python
from stardew.api import (
    AnalysisOptions,
    ReportPredictionOptions,
    analyze,
    load_game_data,
    load_save,
)
from stardew.presentation.json import render_json
from stardew.presentation.text import render_text

state = load_save("/path/to/Farmer_123")
data = load_game_data()

result = analyze(
    state,
    data=data,
    options=AnalysisOptions(
        progress=("cooking", "perfection_tracker"),
        predictions=("geode",),
        prediction_options=ReportPredictionOptions(count=20),
        extras=False,
        bubbles=False,
        artifacts=False,
    ),
)

print(render_text(result, data=data))
json_report = render_json(result)
```

`load_game_data()` loads the bundled catalogs and map geometry. Pass an export
directory, such as `load_game_data("outputs/game-data")`, to add artifact tables.
Use `AnalysisOptions()` for the complete analysis.

### Public contracts

| Model | Purpose |
| --- | --- |
| `GameState` | Immutable saved metadata, players, and world state. |
| `GameData` | Catalogs, map geometry, optional artifact tables, and provenance. |
| `AnalysisOptions` | Feature selection, location filters, and availability handling. |
| `ReportPredictionOptions` | Ranges, player indices, luck inputs, and item filters for report predictions. |
| `AnalysisResult` | Structured progress, predictions, bubbles, artifacts, extras, and diagnostics. |

For `progress` and `predictions`, `None` selects every section, an empty tuple
skips the category, and a tuple of IDs selects specific sections. Extras,
bubbles, and artifacts have independent boolean switches. Set `strict=True`
to raise `FeatureUnavailable` when a requested feature cannot run.

Loaded state, results, and catalogs are immutable. Bundled resources are cached,
and analysis creates fresh calculation contexts. The package includes
`py.typed` for tools that consume its type annotations.

### JSON structure

Text and JSON render the same analysis result. The top-level JSON fields are:

| Field | Contents |
| --- | --- |
| `schema_version` | `2` |
| `save_file`, `metadata` | Save identity, game version, date, seed, and saved flags. |
| `progress` | Section metrics, player progress, collection items, and facts. |
| `predictions` | Feature records with dates, sequences, item IDs, quantities, prices, facts, and alternatives. |
| `bubbles`, `artifacts` | Location-specific events and predicted drops. |
| `extras` | Inventories and supplementary saved data, or `null` when skipped. |
| `diagnostics` | Feature availability messages. |
| `provenance` | Catalog and map sources, plus hashes for exported game tables. |

Missing saved values remain distinct from `0` and `false`. Prediction records
retain IDs and numeric values alongside display names, so consumers can work
directly with facts.

## Architecture

The code separates game rules from file decoding, orchestration, and rendering:

```text
src/stardew/
├── api.py          Public loading and analysis entry points
├── cli/            Command parsing and output coordination
├── domain/         Immutable models, progress rules, predictions, RNG compatibility
├── application/    Feature orchestration, inventories, availability diagnostics
├── infrastructure/ Save loading, game data, XNB/LZX, graphics, atomic file writes
├── presentation/   Text, JSON, and PNG rendering
└── resources/      Bundled catalogs, map geometry, provenance, and fonts
```

The CLI calls the same public API used by Python consumers. Save decoding
produces one shared snapshot; calculations return structured facts; renderers
format those facts for their destination. Loot rules are organized by feature,
with separate modules for geodes, Mystery Boxes, enchantments, prize tickets,
and raccoons.

See [architecture](docs/architecture.md) for layer responsibilities,
[migration](docs/migration.md) for the project's history, and
[progress parity](docs/progress-parity.md) for documented rule corrections.

## Development

### Run the suite and build the package

```sh
uv sync --locked --extra test
uv run --locked --extra test pytest
uv run --locked --extra test python -m build
```

Tests cover the API and CLI, save decoding, progress and inventories, RNG
compatibility, XNB/LZX, graphics, and installed package resources. Fixed
reference fixtures include:

- **2,772 fishing bubble scenarios** captured from the previous C# predictor.
- **400 artifact scenarios** with synthetic tables and captured C# results.
- **3,059 historical records** for all 22 report prediction features across
  ten scenarios, including older versions, multiplayer, and both RNG modes.

GitHub Actions runs the suite on Python **3.11 and 3.13**, builds the distribution,
and tests an installed wheel outside the checkout. Reference inputs are
synthetic; fixture provenance is documented in
[tests/fixtures/README.md](tests/fixtures/README.md).

### Measure performance

```sh
uv run --locked python benchmarks/benchmark_analysis.py --repeat 5
```

The benchmark reports median analysis and JSON rendering times on a synthetic
save with warm caches. Save loading, game-data export, and PNG rendering stay
outside the timed calculations.

Focused analysis skips unrelated work. Progress selection resolves only the
requested sections and their prerequisites; mine predictions calculate the
requested days directly. In the recorded local benchmark, a one-day mine
prediction dropped from approximately **1.15 seconds to 46 milliseconds**.
See [performance](docs/performance.md) for the inputs, measurements, and
profiling commands.

For total report time, add `--profile`:

```sh
uv run --locked stardew report "/path/to/Farmer_123" \
  --only progress --profile -o outputs/progress.txt
```

### Contribute

Bug reports are most useful with the game version, command or API call,
expected result, and actual result. A small synthetic save or a focused
regression case helps reproduce an issue while keeping personal saves local.

Prediction changes can be checked against the captured references in
`tests/fixtures/`. Random draw order, item pool order, and version-specific
behavior are part of prediction compatibility. Keep command examples and
structured output documentation aligned with changes to the public API.

## License and credits

The project uses the [MIT license](LICENSE). Third-party components retain
their own notices and attribution in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md),
[resource licenses](src/stardew/resources/LICENSES.txt), and the bundled
font license.

Catalogs and report rules draw on the MouseyPounds checkup and predictor
references. Map geometry, bubble rules, and artifact rules preserve the
project's earlier predictor work. Source identifiers and hashes accompany
the bundled resources and reference fixtures.
