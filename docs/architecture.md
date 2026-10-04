# Architecture

`src/stardew/domain` contains immutable models, named catalogs, numeric
compatibility operations, progress rules, and prediction calculations. Rules
receive saved facts and injected game data. Save decoding, command-line parsing,
and image generation belong to the surrounding layers.

`domain/models` defines the contracts shared by the API and calculation layers,
including game data, map geometry, saved state, and typed analysis results.
Frequently used player and world fields are decoded once. The immutable
`SaveNode` snapshot retains older fields and extensions for rules that still
need less common saved data.

`domain/predictions/loot` groups geode, mystery-box, enchantment, prize-ticket,
and raccoon rules into separate modules. Selection helpers preserve the original
random draw order and catalog insertion order. Calendar predictions retain their
reference behavior; mines receive explicit day bounds to avoid calculating
unrequested days. RNG instances remain local to each calculation.

`infrastructure/saves` limits reads and decompression to 128 MiB, rejects DTDs,
disables external entities, and converts the XML tree once into `GameState`.
The mutable XML tree stays inside the loader.

`infrastructure/game_data` caches bundled catalogs and map geometry. Exported
XNB tables are loaded per call, carry provenance, and are frozen before analysis.
Locally extracted game tables stay outside the wheel. `infrastructure/xnb`
contains explicit schemas, binary readers, and the LZX decoder.

`application` coordinates features and converts expected unavailability into
diagnostics. Calculation failures propagate. Progress analysis resolves section
dependencies before calculation and returns sections in caller order. The
perfection tracker evaluates every required category and chooses the best
player separately for each category.

`presentation` renders text, JSON, and PNG from structured results. JSON
serializes facts directly. Map rendering uses optional Pillow and local game
graphics; generated labels and diagnostics are in English.

`infrastructure/files` prepares outputs and replaces each file atomically,
including tables and PNGs. A multi-file export can leave earlier files updated
if a later filesystem replacement fails.

`api.py` exposes `load_save`, `load_game_data`, and `analyze`, along with their
input and result models. `cli` uses these entry points. The project uses Python
3.11+, one `pyproject.toml`, one `uv.lock`, and one development environment.
