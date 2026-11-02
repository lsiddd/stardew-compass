# Performance

The main changes remove repeated saved-tree traversal, catalog and capture
copies, unnecessary map loading, and unrequested calendar days. RNG setup uses
precomputed indexes and equivalent signed subtraction. The generator's sequence
and the order of draws remain covered by historical vectors and extreme-seed
regressions.

## Local before/after comparison

Measured on the same machine with Python 3.13, the previous committed version
and the refactored version, and the same local 3,504,785-byte save containing
155,194 snapshot nodes. Stage timings are medians of five runs with garbage
collection before each sample. Analysis reuses loaded state and game data.
The cold figure is a separate fresh-process observation including imports,
loading, full analysis, text and JSON rendering, so it is less statistically
stable than the stage medians.

| Measurement | Before | After |
| --- | ---: | ---: |
| Save loading | 644.905 ms | 602.288 ms |
| Full loaded analysis | 1,434.205 ms | 627.109 ms |
| Text rendering | 16.873 ms | 18.040 ms |
| JSON rendering | 31.208 ms | 28.352 ms |
| Cold pipeline observation | 2,353.595 ms | 1,522.417 ms |
| Python peak allocations: load + analysis + JSON | 128.006 MiB | 45.506 MiB |

Loaded analysis was about 56% faster; peak traced allocations were about 64%
lower. The cold pipeline was about 35% faster in this observation. Text adds
assumptions and coverage information, so its small increase also includes more
output. These are local measurements, not performance guarantees.

Both versions returned 27 progress sections, 22 prediction sections, 692
prediction records, 26 fishing events and 9 artifact spots on that save. Equal
counts alone do not prove parity; the tests separately cover actual facts and
the documented garbage-can and train corrections.

The memory reduction includes an input-boundary fix: reading with a 128 MiB
maximum requested a buffer of that size even for a small save. Chunked bounded
reads now grow with actual contents while still detecting oversized input.
Shared indexes are limited to the tags and names used by calculations. They do
not retain every snapshot node a second time in tag lists.

## Repeat the benchmark

The committed benchmark defaults to a synthetic save with no personal data:

```sh
uv run --locked python benchmarks/benchmark_analysis.py --repeat 5
```

For a larger synthetic fixture, add placed objects. Memory tracing runs
separately from timed calculations:

```sh
uv run --locked python benchmarks/benchmark_analysis.py --objects 10000 --repeat 5 --cold --memory
```

To measure a local save and its exported game tables:

```sh
uv run --locked python benchmarks/benchmark_analysis.py --save /path/to/Farmer_123 --data-dir outputs/game-data --repeat 5 --cold --memory
```

Output includes byte/node counts, loading, summary, one-day and 28-day mines,
full analysis and both renderers. `--cold` launches a fresh CLI process for each
sample and includes imports, resource loading and JSON output. `--memory` reports
peak Python allocations for loading, analysis and JSON; it excludes already
loaded game data and native Pillow allocations. The synthetic analysis skips
map-dependent predictions; a supplied local save enables bubbles, and supplied
game tables enable artifacts. The cold CLI uses its normal full-report defaults.

The benchmark never prints save contents. Timing varies with hardware, garbage
collection, version, player count, interval and saved objects. Avoid running
CPU-heavy tests or builds concurrently with timing samples.

## Profile a save

`report --profile` reports elapsed time to stderr. Use a profiler for locating
costs, and wall-clock samples for measuring speed:

```sh
uv run --locked python -m cProfile -s cumulative -m stardew predict mines /path/to/Farmer_123 --start 1 --count 1 -o outputs/mines.txt
```

Full prediction windows still perform the requested RNG work. No global RNG
cache is used: almost every seed in the measured full report was unique.
