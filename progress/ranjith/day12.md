# Ranjith Day 12 - feat(eval): add CSV export to FederatedMetricsTracker

## Tasks Completed
* Implemented `export_csv(filepath)` using Python `csv.DictWriter`.
* Exports columns: round, global_dice, dice_ncr, dice_ed, dice_et, hd95, loss.
* Auto-saves to `results/federated_metrics.csv` after every 5 rounds.

## Files Modified/Created
* `eval/federated_metrics.py` — `export_csv()` method (20 lines)
* `results/` — directory created automatically

## Notes & Challenges
* CSV NaN values exported as empty string for Excel compatibility.

## Tomorrow's Plan
* Create matplotlib convergence plot generation.
