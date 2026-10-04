# Fixed reference fixtures

Generated on 2026-09-12 before removing the C# implementation. Original source
SHA-256 hashes are in reference-sources.json. The hashes identify the prior
source snapshot; this fixture suite never executes C#.

- bubbles.json.gz: original BubblePredictor results for 11 maps, nine days,
  legacy/hashed RNG, two panning labels, seven seeds (2,772 records). Seeds are
  390938626, 0, 1, -1, 4294967295, Int64.MaxValue and Int64.MinValue.
  Days are 1, 4, 5, 13, 15, 28, 112, 113 and 200. Year=2, version=1.6.15,
  farm=Riverland; timesFished=0 before day 15, otherwise 100. The two panning
  labels intentionally have identical outputs: panning follows bubble draws.
  Before capture, all original 396 oracle comparisons passed.
- random.json.gz: System.Random(seed), 20 repetitions of Next(), NextDouble(),
  Next(100), Next(-100,100), Next(Int32.MinValue,Int32.MaxValue), Next(0),
  Next(3,3), for seven seeds. Values are captured, not calculated by Python.
- artifacts.json and artifact-*.json: 400 synthetic C# predictions using the
  supplied synthetic tables. Inputs vary locations, seeds, legacy mode, books,
  enchantments, counters, conditions, stacks and extra drops. No personal state
  or game tables are included.
  Captured Portuguese presentation labels remain in the reference files;
  `test_artifacts.py` translates those labels when checking English output.
  Item IDs, quantities, runtime alternatives and random draws remain unchanged.
- objects-synthetic.xnb / locations-synthetic.xnb: synthetic XNB v5 streams
  written from explicit field/property order and decoded by the installed
  MonoGame ContentManager using GameData 1.6.15.24356. Their JSON files are the
  System.Text.Json outputs of that independent decode. They exercise all 14
  classes, inheritance, null/default objects, nullable values, lists,
  dictionaries, enums, float32, negative rectangle coordinates/dimensions,
  recipe/random-item ID fallback and calculated music IDs.

LZX test streams are constructed with known canonical codes and literal/match
payloads. Expected bytes are explicit. They cover verbatim and aligned blocks,
uncompressed blocks, repeated offsets, three-frame window wrap, extended frame
headers and malformed input. Real compressed game files were separately
compared byte-for-byte with MonoGame; those private data are not fixtures.

Unified report references:

- `report-rng.json`: seeded RNG and string hash vectors preserved from the
  report project's original tests.
- `progress_reference_v2.json`: synthetic reference facts covering all 27
  progress sections. Detailed parity and corrected source defects are recorded
  in `docs/progress-parity.md`.
- `report-predictions.json.gz`: 3,059 historical factual records for all 22
  prediction tabs in ten synthetic scenarios, captured before replacing the
  old implementation. Versions 1.2–1.6.15, multiplayer, legacy/hashed RNG,
  negative seeds and large game/player IDs are represented. Presentation and
  new identity fields are checked separately from historical raw calculations.
