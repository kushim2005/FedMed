# Ranjith Day 11 - feat(eval): implement HD95 tracking with NaN-safe aggregation

## Tasks Completed
* Added `HausdorffDistanceMetric(percentile=95)` from MONAI to `FederatedMetricsTracker`.
* NaN handling: `hd95 if hd95 is not None and not np.isnan(hd95) else None`.
* Stores NaN-free HD95 values; rounds with tiny tumors record `null` in JSON.

## Files Modified/Created
* `eval/federated_metrics.py` — HD95 tracking (20 lines added)

## Notes & Challenges
* HD95 is undefined when predicted mask is empty; added empty-mask guard in `compute_dice_score()`.

## Tomorrow's Plan
* Add CSV export to FederatedMetricsTracker.
