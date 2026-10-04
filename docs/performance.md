# Performance

Analysis calculates requested work at the feature boundary. A single-day mine
prediction runs that day directly. Progress selection resolves prerequisites
and skips unrelated sections. Perfection still evaluates every contributing
category before selecting the best player for each category.

Local measurements during this refactor used Python 3.13, synthetic saves,
preloaded state and data, and median wall-clock timings. The before and after
runs used the same machine and inputs:

| Calculation | Before | After |
| --- | ---: | ---: |
| Summary only | 2.650 ms | 0.014 ms |
| Mines, one day | 1,149.829 ms | 45.683 ms |
| Mines, 28 days | 1,142.852 ms | 1,127.469 ms |
| Complete analysis, excluding bubbles and artifacts | 1,311.351 ms | 1,259.230 ms |

The largest gain comes from skipping unrequested work. Timing varies with
hardware, game version, save contents, selected features, and interval length.

## Repeat the benchmark

The committed benchmark uses a generated synthetic save and prints median
milliseconds. Module imports and bundled caches are warmed before timing.

```sh
uv run --locked python benchmarks/benchmark_analysis.py --repeat 5
```

It measures calculation and JSON rendering separately. Save loading, local
game exports, and PNG rendering are outside the timed region. The Summary
fixture in the recorded comparison included additional synthetic progress
fields; the committed benchmark uses one shared fixture for all measurements.

## Profile a save

The CLI's `--profile` reports total elapsed time to stderr. For a breakdown
of function costs, use Python's profiler:

```sh
uv run --locked python -m cProfile -s cumulative -m stardew predict mines /path/to/Farmer_123 --start 1 --count 1 -o outputs/mines.txt
```

Use wall-clock benchmarks to compare speed. Profiler timings include tracing
overhead and help locate the work responsible for that speed.

## Compatibility

Regression tests compare explicit mine intervals against full calendar facts
and verify that small intervals initialize fewer RNG instances. Progress tests
verify independent section selection and multiplayer perfection prerequisites.
An expanded migration check compared 23,000 loot records in 100 scenarios
against the previous implementation, including sequence offsets 0 and 500.
Random draw order, item pool insertion order, quantities, and IDs were preserved.
