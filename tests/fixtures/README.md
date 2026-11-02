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

## Corrections against the installed game

The 2026-11-02 audit compared the predictor with the installed Stardew Valley
1.6.15 assembly and its decoded data. The historical prediction fixture remains
unchanged: it records the previous predictor, including its defects, and is not
a game oracle. `test_report_predictions.py` keeps 146 of its 220 feature/scenario
comparisons active. The other 74 are explicit parameterized skips with concrete
reasons; no skip is decided by comparing the current output with the fixture.

| Historical comparison invalidated | Scenarios | Reason |
| --- | --- | --- |
| Raccoon requests/rewards | All 10 | Reward four is five Fairy Dust; weighted pools reject duplicate item IDs. |
| Weather | All 10 | Rain/Storm can depend on session RNG, and calendar overrides take priority. |
| Desert Festival | All 10 | Cactus uses player seed components; selection obeys eligibility and draw order. |
| Statues | All 10 | Guaranteed rain prevents Butterfly spawns; negative odd game IDs require C# division toward zero. |
| Trains | Nine; largest hashed ID still compared | Festivals suppress trains; negative legacy components require C# truncation. |
| Mines | Four 1.6+ cases | Forced Skull Cavern chest floors are excluded; eligible alternate layouts affect floor types. |
| Night events | Four 1.6+ cases | Fairy Rose alternatives and one-time saved world flags affect candidates. |
| Enchantments and Winter Star | Four 1.6+ cases each | Int64 values convert to double before the seed remainder; Winter Star filters donor candidates. |
| Geodes, mystery boxes, cart, Krobus, Sandy, wallpaper, bookseller, trash | Negative legacy only | Integer division and truncation differ from the historical fractional/floor operations. |
| Remixed mine chests | Largest hashed ID only | The game converts the ID to double before multiplying it by 512. |

Corrected behavior is covered by explicit game-rule counterexamples in
`test_loot_game_rules.py`, `test_calendar_game_rules.py`, and
`test_game_seed_rules.py`. The seed vectors include values captured by invoking
the installed assembly, rather than regenerating expected values with Python.
Prize tickets and Calico Jack still match all ten historical samples and retain
their comparisons; a rule correction does not invalidate samples that still
have the same result.

The historical baseline now states its formerly implicit assumptions: remixed
mine rewards, quarry already visited, global mine progress 120, theater already
visited, fishing level 10, house level zero, artifact discovery complete, and
the first coconut and Golden Helmet already collected. Separate tests cover
those gates when the flags differ or are missing. New identity, provenance and
uncertainty fields are checked by rule/API tests rather than this old capture
format. Calico Jack's formerly unset threshold is normalized to its known
0.0005 minimum for the fixture's fixed luck. Raw scenarios deliberately call
all functions even on older version labels; these do not claim that 1.6-only
features existed in earlier games.

`game-enchantment-rules.json` contains 54 synthetic captures from the installed
assembly's `BaseEnchantment.GetAvailableEnchantmentsForItem` and
`Utility.CreateRandom` on .NET 6. Hoe, WateringCan and Pan cover upgrade levels
0, 3 and 4; fresh/current/two-entry histories; hashed and legacy RNG. The file
records the assembly hash and synthetic game/player IDs. Tests normalize the
internal enchantment name `Expansive` to the public label `Reaching`; expected
pools and selections come from the original methods, not the predictor.

`game-tool-serialization.json` records `XmlSerializer` roundtrips of the original
Hoe type, fresh and enchanted, plus the original method's restored pool and
selection. Empty enchantment/history lists are omitted; populated lists use
repeated `enchantments` and `previousEnchantments` elements. These captures
protect the production save format alongside the older synthetic wrapper form.


Installed-game numeric observations:

- `game-seed-boundaries.json` captures four draws from the original
  `Utility.CreateRandom` for signed Int64 boundaries, a negative odd ID and
  the repository's historical seed 390938626, in both legacy and hashed modes.
  Its source identifies the DLL SHA-256 and .NET 6 runtime.
- `test_game_seed_rules.py` additionally preserves direct DLL captures for
  large player IDs, two-stage cactus seeds and floating cancellation. Legacy
  additions use C# left-to-right rounding, including on Python 3.12+ where
  `sum()` would compensate rounding differently.
- `game-map-rules.json` and `test_map_game_rules.py` preserve map/seed/luck
  observations. The average-luck regression executes the same accumulation
  order as `FarmerTeam.AverageDailyLuck`; its expected value was independently
  captured with six in-memory farmers in the original DLL.
- `game-geode-results.json` captures 240 results from the unmodified
  `Utility.getTreasureFromGeode`: opening numbers 468–487, six container types,
  hashed and legacy RNG. It identifies the DLL and Objects.xnb hashes and the
  exact input flags. It uses a small in-memory world without opening or saving
  a game session. It does not reproduce the Python algorithm or the retired
  predictor. Clint's first-coconut override is separately covered by menu-rule
  regressions; the capture has that coconut already opened.

- `game-trash-seeds.json` contains four direct day-save RNG captures for
  JodiAndKent, with the original string hash, seed and first draws. An odd
  ID in legacy mode with a negative sum and an odd ID above 2^53 catch
  division performed as a double before the game's integer division.

These captures do not contain a personal save or copied game tables, and tests
consume the fixed observations without loading an installed game.
