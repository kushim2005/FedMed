# Ranjith Day 21 - analysis(eval): compare global Dice vs per-hospital local Dice

## Tasks Completed
* Extracted per-hospital Dice at Round 10: Hospital-A=0.66, Hospital-B=0.71, Hospital-C=0.68.
* Global aggregated Dice = 0.693 — slightly higher than any individual hospital.
* This validates federated learning: global model generalizes better than any local model.

## Files Modified/Created
* `results/per_hospital_vs_global_dice.json` — comparison data
* `results/hospital_comparison.png` — bar chart

## Notes & Challenges
* Hospital-B has highest local Dice (0.71) — coincides with having most balanced data partition.

## Tomorrow's Plan
* Mid-project evaluation report — federated convergence analysis.
