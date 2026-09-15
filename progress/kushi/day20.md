# Kushi Day 20 - perf(server): profile memory usage during weight aggregation

## Tasks Completed
* Profiled `aggregate_fit()` with `tracemalloc` during 3-client aggregation.
* Peak memory during aggregation: 2.1 GB (3D UNet weights × 3 clients).
* Identified: numpy stacking of all client tensors allocates O(N × model_size) memory.

## Files Modified/Created
* `server/fl_server_v2.py` — added `tracemalloc` profiling in debug mode

## Notes & Challenges
* Memory is acceptable for 3 clients; Week 3 encryption will add overhead.

## Tomorrow's Plan
* Full TLS end-to-end test: 3 hospitals × 10 FL rounds.
