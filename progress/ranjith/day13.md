# Ranjith Day 13 - feat(eval): implement matplotlib convergence plot generation

## Tasks Completed
* Implemented `plot_convergence(save_path)`: 2-panel figure — global Dice + per-class Dice.
* Applied Gaussian moving average smoothing (window=3) to global Dice curve.
* Saves `results/convergence.png` at 150 DPI; uses `matplotlib.use("Agg")` for headless.

## Files Modified/Created
* `eval/federated_metrics.py` — `plot_convergence()` method (50 lines)

## Notes & Challenges
* Moving average requires at least 3 rounds; added length guard before applying.

## Tomorrow's Plan
* Validate FedAvg aggregation math with a weighted average correctness test.
