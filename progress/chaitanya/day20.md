# Chaitanya Day 20 - FedProx (Dice=0.69) beats FedAvg (Dice=0.67) on val

## Tasks Completed
* Ran 5-round FL with FedProx (mu=0.01) and FedAvg side-by-side
* FedProx val Dice=0.69 vs FedAvg val Dice=0.67 — +2pp improvement
* Logged results to `results/fedprox_vs_fedavg.csv`; plotted comparison bar chart

## Files Modified/Created
* `eval/federated_metrics.py` - `compare_strategies()` function added
* `results/fedprox_vs_fedavg.csv` - per-round Dice for both strategies
* `results/fedprox_vs_fedavg_plot.png` - matplotlib bar chart saved

## Notes & Challenges
* FedProx convergence was smoother; FedAvg had Dice dip in round 3 due to data heterogeneity

## Tomorrow's Plan
* Document all training improvements in docs/week2_pipeline.md
