# Chaitanya Day 22 - Mid-project benchmark: federated Dice=0.69 vs centralized Dice=0.72

## Tasks Completed
* Ran centralized baseline (all 3-hospital data pooled): val Dice=0.72
* Federated (FedProx, 5 rounds): val Dice=0.69; gap=3 percentage points
* Documented federated-vs-centralized analysis in `results/midpoint_benchmark.md`

## Files Modified/Created
* `eval/federated_metrics.py` - added centralized comparison logic
* `results/midpoint_benchmark.md` - full benchmark table and gap analysis

## Notes & Challenges
* 3% gap is within acceptable range for privacy-preserving approach; team agreed to continue

## Tomorrow's Plan
* Generate per-round training loss curves using matplotlib
