# Ranjith Day 9 - feat(eval): implement FederatedMetricsTracker class

## Tasks Completed
* Created `eval/federated_metrics.py` with `FederatedMetricsTracker` class.
* `update(round_id, global_dice, dice_ncr, dice_ed, dice_et, hd95, loss, hospital_dice)`.
* `rounds` list accumulates all metrics; `summary()` returns best round info.

## Files Modified/Created
* `eval/federated_metrics.py` — FederatedMetricsTracker (100 lines)

## Notes & Challenges
* Used `Optional[float]` for HD95 since it can be None for small regions.

## Tomorrow's Plan
* Add per-class Dice tracking (NCR, ED, ET) per FL round using MONAI DiceMetric.
