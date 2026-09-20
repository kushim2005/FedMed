# Chaitanya Day 25 - Hyperparameter tuning: LR 1e-3 → 1e-4, Dice improves to 0.71

## Tasks Completed
* Updated `config/week2_config.yaml` `lr: 1e-4`; re-ran 5-round FL with FedProx
* Val Dice improved from 0.69 → 0.71 with smaller LR; ET Dice gain most significant (+2 pp)
* Saved tuned checkpoint to `checkpoints/global_best_lr1e4.pth`

## Files Modified/Created
* `config/week2_config.yaml` - `lr` updated to `1e-4`
* `checkpoints/global_best_lr1e4.pth` - new best model checkpoint
* `results/hyperparam_tuning_log.csv` - LR sweep results appended

## Notes & Challenges
* Training time increased slightly (~8% per round); acceptable trade-off for Dice gain

## Tomorrow's Plan
* Final model evaluation on full validation partition
