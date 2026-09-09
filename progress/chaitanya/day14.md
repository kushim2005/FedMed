# Chaitanya Day 14 - Benchmark local vs federated Dice after 5 FL rounds

## Tasks Completed
* Ran full FL loop: 3 hospitals × 5 rounds with FedAvg aggregation
* Results: local Dice=0.64 (Hospital-A only) vs federated Dice=0.67 (+4.7%)
* Logged comparison table to `results/fedavg_vs_local_benchmark.md`

## Files Modified/Created
* `eval/federated_metrics.py` - added `compare_local_vs_federated()` function
* `results/fedavg_vs_local_benchmark.md` - benchmark results table

## Notes & Challenges
* Round 1 global model hurt Hospital-A Dice transiently due to heterogeneous data

## Tomorrow's Plan
* Implement model checkpointing to save best global model each round
