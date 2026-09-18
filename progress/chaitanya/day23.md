# Chaitanya Day 23 - Generate training loss curves per FL round using matplotlib

## Tasks Completed
* Wrote `eval/federated_metrics.py:plot_loss_curves()` to read per-round loss CSVs
* Generated per-hospital and global loss curves across 5 FL rounds
* Saved figures to `results/loss_curve_round*.png` (5 files)

## Files Modified/Created
* `eval/federated_metrics.py` - `plot_loss_curves()` using matplotlib subplots
* `results/loss_curve_round1.png` through `results/loss_curve_round5.png`

## Notes & Challenges
* Hospital-C loss curve noisier than A/B; likely due to smaller partition (Dirichlet α=0.5)

## Tomorrow's Plan
* Submit model comparison report (centralized vs federated) to team
