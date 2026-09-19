# Ravi Day 24 - perf(benchmark): 10 FL rounds timing benchmark

## Tasks Completed
* Ran full 10-round FL simulation: total time 42.3 minutes (CPU-only).
* Per-round avg: 4.2 min (data loading: 0.8 min, training: 3.1 min, aggregation: 0.3 min).
* Profiled: DataLoader is bottleneck for first epoch (cold cache); subsequent epochs faster.

## Files Modified/Created
* `results/benchmark_10_rounds.txt` — timing breakdown per round

## Notes & Challenges
* GPU training would reduce round time from 4.2 min to ~0.9 min (estimated 4.7x speedup).

## Tomorrow's Plan
* Update README.md with Week 2 setup and run instructions.
