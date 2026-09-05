# Ranjith Day 10 - feat(eval): add per-class Dice tracking (NCR, ED, ET) per FL round

## Tasks Completed
* Integrated MONAI `DiceMetric(include_background=False)` for per-class computation.
* Separate Dice for NCR (necrotic core), ED (edema), ET (enhancing tumor).
* Connected tracker to server `aggregate_evaluate()` callback via metrics dict.

## Files Modified/Created
* `eval/federated_metrics.py` — per-class Dice (added 30 lines)

## Notes & Challenges
* MONAI DiceMetric requires one-hot encoded predictions; added `AsDiscrete(argmax=True, to_onehot=4)`.

## Tomorrow's Plan
* Implement HD95 per-round tracking with NaN handling.
