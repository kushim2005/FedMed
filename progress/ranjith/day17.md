# Ranjith Day 17 - feat(eval): add per-hospital local Dice tracking

## Tasks Completed
* Added `hospital_dice: Dict[int, float]` field to `update()` call.
* Tracker now records per-hospital Dice per round alongside global Dice.
* `plot_convergence()` updated: 3rd panel showing Hospital-A/B/C local Dice per round.

## Files Modified/Created
* `eval/federated_metrics.py` — hospital_dice tracking + 3-panel plot

## Notes & Challenges
* Hospital Dice comes from client `evaluate()` return value; connected via Flower metrics dict.

## Tomorrow's Plan
* Create metrics summary CSV report generator.
