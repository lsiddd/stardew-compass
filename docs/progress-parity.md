# Progress rule parity

The migration preserves 27 progress sections and calculates perfection using
the original weights, catalogs, counts, and goals. Calculations receive an
immutable saved snapshot and produce structured facts shared by text and JSON.

The reference is MouseyPounds' checkup, revision `8e48aa1`, and its port retained
in this repository's Git history.
[`progress_reference_v2.json`](../tests/fixtures/progress_reference_v2.json)
records a synthetic 1.6.15 fixture: 25 count/goal pairs, the Summary calendar,
and Animals facts, covering all 27 exposed sections. Values were checked
against the previous engine's rules and output. Names and IDs are synthetic.

[`test_progress.py`](../tests/unit/test_progress.py) also checks version-specific
catalogs from 1.2 through 1.6, mod recipes, Wedding Ring exclusion, qualified fish
IDs, mine stardrops, walnut reward limits, family relationships, social events,
and the Secret Note #14 statue at its original position. Additional save and
mod combinations can extend these regression fixtures.

## Recorded corrections

These changes follow explicit intentions in the previous engine or requirements
of the unified models. Other rules retain their original goals and weights.

| Case | Previous engine | Native implementation | Regression test |
| --- | --- | --- | --- |
| `gotMaxStamina` with fewer than seven stardrop markers | The section showed the override as complete, but perfection used only the marker count. | The flag grants the category's 10 percentage points. Marker counts, missing IDs, and the goal of seven remain explicit. | `test_stamina_override_changes_perfection_without_changing_marker_facts` |
| Multiplayer house upgrades | `parsePlayerFamily` defined host = 3 and farmhand = 2, but `parseFamily` passed `isHost = True` for farmhands too. | The host needs three upgrades; each farmhand needs two. | `test_host_and_farmhand_have_distinct_upgrade_goals` |
| Farmhands without `UniqueMultiplayerID` | Individual records shared an empty key. | Local identities `player_1`, `player_2`, etc. keep statistics separate while retaining the absent saved ID. | `test_missing_player_ids_keep_individual_statistics` |
| No eligible friendships | The section calculated `0 / 0`; the global contribution stayed at zero because comparison with that value failed. | Count, goal, and percentage are zero; completion is false. Perfection contributes zero and records a diagnostic. | `test_zero_friendships_contribute_zero_to_perfection` |
| Integer statistics above `2^53` | Numeric conversion through floating point could round the value. | Modern rules reuse exact integers from `PlayerState.stats`. | `test_progress_uses_exact_loaded_player_statistics` |
| All players at zero with a positive goal | The selector retained zero percentage with an empty identity. | The first player wins the tie; the real goal and zero contribution remain explicit. | `test_zero_perfection_keeps_category_goals` |

The original stamina notice states:

> Stamina will override stardrop marker count for achievements and perfection.

The correction applies this override to perfection while keeping collection
facts based on saved markers.

## Calculation isolation and dependencies

Each analysis creates a fresh context. Requested sections and prerequisites are
calculated in canonical order before returning results in caller order. The
perfection tracker requires skills, monsters, stardrops, social progress,
cooking, crafting, fishing, basic shipping, and walnuts.

`test_text_and_json_preserve_progress_details` checks XP and next-level goals,
relationship points and status, event IDs, bundle quantities and quality, and
upgrade costs in both renderers.

`test_perfection_selection_order_and_call_isolation` compares a full analysis
with reordered selections and repeated calls.

`test_perfection_uses_best_player_per_category` verifies that different players
can supply different perfection categories: the best cook contributes 10 points
and the best shipper contributes 15 points.

To repeat the verification:

```sh
uv run --locked --extra test pytest tests/unit/test_progress.py -q
```
