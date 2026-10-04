# Migration from the previous projects

The `stardew-report` history is retained at the root of `stardew`. Previous
implementations served as migration references and are archived locally under
`outputs/migration-reference/legacy/`. Git also retains the original commits.

The unified toolkit exposes 27 progress sections, 22 report prediction features,
fishing bubbles, artifact spots, inventories, XNB exports, and PNG maps. The
initial report tests passed all 21 cases. The migration preserved C# reference
outputs for 2,772 bubble cases and 400 artifact cases, along with synthetic
XNB/LZX and graphics fixtures.

Personal reference reports, maps, and saves remain under ignored local output
directories. Exported local game tables are stored under `outputs/game-data`
and stay outside the distribution.

Use `stardew report`, `stardew predict`, and `stardew data export` in place of
the previous commands and report-generation shell script. Text-based section
JSON has been replaced by structured facts in schema v2.

Documented progress rule corrections and their regression tests are listed in
[progress-parity.md](progress-parity.md).

The root now uses the `.venv` environment and the `stardew` command. The two
previous virtual environments were removed during the migration.
