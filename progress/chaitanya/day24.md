# Chaitanya Day 24 - Submit model comparison report to team

## Tasks Completed
* Compiled `results/model_comparison_report.md`: centralized vs federated, per-class Dice table
* Included WT/TC/ET Dice breakdown: federated WT=0.82, TC=0.71, ET=0.58 (vs centralized 0.85/0.74/0.61)
* Shared report in team Slack and scheduled review meeting for Day 26

## Files Modified/Created
* `results/model_comparison_report.md` - full per-class and aggregate Dice analysis

## Notes & Challenges
* ET class shows largest gap (3 pp); ET tumour region smallest and most affected by non-IID split

## Tomorrow's Plan
* Hyperparameter tuning: try LR=1e-4 and observe Dice impact
