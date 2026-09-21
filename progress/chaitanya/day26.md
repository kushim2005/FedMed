# Chaitanya Day 26 - Final model evaluation on full validation partition

## Tasks Completed
* Loaded `checkpoints/global_best_lr1e4.pth` and ran inference on full val set (all 3 hospitals)
* Final metrics: mean Dice=0.71, HD95=12.4 mm, Sensitivity=0.78, Specificity=0.94
* Saved per-case Dice to `results/final_val_per_case.csv` (180 cases)

## Files Modified/Created
* `eval/federated_metrics.py` - `run_final_evaluation()` added for full-partition eval
* `results/final_val_per_case.csv` - per-case Dice, HD95 saved
* `results/final_val_summary.md` - aggregated stats table

## Notes & Challenges
* 3 cases with Dice<0.50 (all GBM rim); flagged for Week 3 post-processing investigation

## Tomorrow's Plan
* Code review of train/federated_train.py with Ravi
