# Ranjith Day 22 - docs(report): mid-project evaluation report — convergence analysis

## Tasks Completed
* Wrote `docs/midproject_eval_report.md`: convergence curves, per-class Dice, hospital comparison.
* Key finding: federated model converges by Round 8 (Dice plateaus at 0.693).
* FedProx reduces per-hospital Dice variance vs FedAvg (std: 0.024 vs 0.038).

## Files Modified/Created
* `docs/midproject_eval_report.md` — 4-page evaluation report

## Notes & Challenges
* Convergence by Round 8 means we can reduce `num_rounds` from 10 to 8 to save compute.

## Tomorrow's Plan
* Generate confusion matrices for each hospital partition.
