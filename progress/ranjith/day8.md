# Ranjith Day 8 - design(eval): design federated metrics tracking schema

## Tasks Completed
* Designed per-round metrics schema: round_id, global_dice, dice_ncr, dice_ed, dice_et, hd95, loss, hospital_dice.
* Reviewed existing `eval/metrics.py` (Week 1) — `SegmentationEvaluator` class with MONAI DiceMetric.
* Planned `FederatedMetricsTracker` class API: `update()`, `export_csv()`, `plot_convergence()`.

## Files Modified/Created
* `docs/metrics_schema.md` — draft metrics schema (20 lines)

## Notes & Challenges
* HD95 can be NaN for very small tumor regions; must handle gracefully.

## Tomorrow's Plan
* Implement `eval/federated_metrics.py` — FederatedMetricsTracker class.
