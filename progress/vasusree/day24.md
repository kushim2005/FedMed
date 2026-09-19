# Vasu Sree Day 24 - perf(docker): 10 FL rounds performance test in optimized containers

## Tasks Completed
* Re-ran 10-round simulation with optimized containers — total time: 36.8 min (vs 38 min before).
* 1.2 min improvement from smaller image (faster Docker layer loading and startup).
* Per-round timing: avg 3.7 min (data: 0.7 min, training: 2.8 min, aggregation: 0.2 min).

## Files Modified/Created
* `results/docker_perf_optimized.txt` — timing comparison before/after optimization

## Notes & Challenges
* Startup time reduced from 12s to 7s per container after slim image optimization.

## Tomorrow's Plan
* Write `docker/README.md` step-by-step deployment guide.
