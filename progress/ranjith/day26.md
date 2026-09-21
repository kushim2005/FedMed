# Ranjith Day 26 - fix(eval): resolve HD95 NaN issue for small tumor regions

## Tasks Completed
* Root cause: MONAI HD95 returns NaN when predicted mask is all-zero (no tumor predicted).
* Fix: in `compute_dice_score()`, check if predicted mask is empty before computing HD95.
* Updated `FederatedMetricsTracker.update()` to skip NaN HD95 values in mean calculation.

## Files Modified/Created
* `eval/federated_metrics.py` — NaN guard in HD95 aggregation
* `eval/metrics.py` — empty-mask check before HD95 computation

## Notes & Challenges
* 3 out of 369 cases had all-zero predictions in early rounds (model not yet converged).

## Tomorrow's Plan
* Code cleanup and final docstrings in `eval/federated_metrics.py`.
