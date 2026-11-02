# Architecture

`api.py` exposes `load_save`, `load_game_data`, and `analyze`. The CLI uses the
same entry points. `domain` owns calculations and immutable facts;
`infrastructure` owns files, XML, JSON, XNB/LZX and graphics; `application`
coordinates requested features; `presentation` renders results. Architecture
tests prevent domain imports of infrastructure or renderers and keep file writes
out of application calculations.

## Saved state and scalar contracts

The loader decodes commonly used player and world fields once: collections,
friendships, experience, skills, placed objects, buildings, NPCs and active orders.
A small `SaveIndex` contains the object names and tags used by multiple rules.
The immutable `SaveNode` snapshot retains uncommon legacy and extension fields;
its traversal is iterative, `find` stops at the first match, and a bounded cache
stores compiled paths rather than saves or query results.

`GameVersion` normalizes equivalent forms such as `1.6` and `1.6.0`. Integer
counters preserve their original precision. Options reject invalid types and
non-finite luck at the boundary. Missing multiplayer IDs remain missing: progress
uses a local label, while predictions that seed with a player ID explain their
unavailability instead of inventing a seed.

## Prediction execution

`domain/predictions/registry.py` declares each feature's identity, scope, minimum
version and range unit. World features execute once, player features receive the
selected player's facts, and mixed features select player-specific outputs
inside one world calculation. `windows.py` plans daily, weekly, monthly, yearly,
sequence and Calico Jack requests explicitly. Independent daily rules calculate
only the intersection with requested dates; weekly shops retain their original
stock generation order.

`features/` contains individual calendar, shop and event rules. `loot/` contains
geode, mystery-box, enchantment, prize-ticket and raccoon rules. These functions
retain the reference RNG consumption and ordered pools. Compatibility arithmetic
in `numeric` explicitly distinguishes report floor/floating-point seed handling
from C# integer truncation and signed remainders. Constructor optimizations are
checked against the reference algorithm, including extreme signed seeds.

Calculation-local mutable arrays never become shared state. A feature emits
facts to `records/`, whose feature-specific builders immediately create immutable
public records. Production does not retain or deep-copy a second history of
algorithm locals. Raw captures and the old import modules remain as adapters
for historical parity tests. Some legacy rules still use named catalog pools
and compatibility facts internally; changes to those rules must preserve draw
order and ambiguity information, rather than guessing missing item identities.

Artifact conditions are compiled and validated before evaluation. Stable drop
ordering and artifact pools are prepared once per predictor, while evaluation
preserves short-circuiting and the original random draws. Unsupported external
conditions are errors even when an earlier condition would happen to be false.

## Progress and orchestration

Progress selection resolves dependencies and skips unrelated categories. Each
contributing rule returns an explicit `CompletionContribution`; it does not
modify a shared perfection accumulator. The perfection calculation consumes
those results and independently selects the best player for every category.
Contributions are internal data and are excluded from the public wire format.

Application orchestration converts expected unavailability into diagnostics and
lets internal calculation errors propagate. Provenance includes engine and rule
versions, requested features, player selection, luck assumptions, filters and
observed prediction coverage. Empty requested results can be distinguished from
features that were skipped or unavailable.

## Input and output boundaries

Save input and decompression are bounded to 128 MiB. XML parsing rejects DTDs and
external entities. JSON/map input is bounded to 64 MiB; XNB input to 128 MiB and
its declared decompressed output to 256 MiB. Reads grow with actual contents,
without preallocating the maximum allowed input. External maps and artifact
tables are validated with source/location diagnostics before calculation.
Bundled resources are cached and immutable. `load_game_data(include_maps=False)`
skips geometry for reports that do not need fishing bubbles.

New table exports include `manifest.json` with hashes of every JSON payload,
format version, inspected game version and locale. All payloads are staged
before publication, and the manifest is replaced first. A partial filesystem
failure is detected on the next read through missing files or hash mismatch.
Readers reject the partial set; they do not automatically roll it back. Older
exports with provenance but no manifest remain supported and are explicitly
marked as unverified by a manifest.

Text, JSON and PNG share the same calculation results. Schema v2 has an explicit
field allowlist and a packaged JSON Schema at
`resources/report-v2.schema.json`; adding a dataclass field cannot silently
expose it in reports. Text includes collection categories and enchantments.
PNG output stages one encoded figure at a time and publishes only after all
figures succeed, reducing peak image memory. Replacing each individual file is
atomic; a filesystem failure during batch publication can still replace only
part of a PNG batch.

## Verification

The test suite includes fixed historical vectors, boundary and multiplayer
regressions, interval composition, incomplete exports, layer boundaries and
schema validation. Ruff checks all production, test and tooling files. Mypy
checks models, scalar contracts, progress, application/CLI coordination and
JSON/file boundaries; the translated prediction internals are not fully
statically typed. CI runs Python 3.11 and 3.13 on Linux and Windows and tests the
built wheel from a temporary directory outside the checkout.
