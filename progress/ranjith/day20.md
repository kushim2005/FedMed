# Ranjith Day 20 - analysis(eval): validate Dice scores against BraTS benchmark ranges

## Tasks Completed
* Ran full 10-round FL simulation; collected per-class Dice at Round 10.
* ET Dice = 0.71, ED Dice = 0.74, NCR Dice = 0.58 — all within expected BraTS FL benchmark range.
* Compared against BraTS 2021 leaderboard: centralized SOTA ET ≈ 0.83; federated gap is expected.

## Files Modified/Created
* `results/brats_benchmark_comparison.md` — federated vs centralized benchmark

## Notes & Challenges
* NCR Dice=0.58 is lower than ET/ED; small necrotic regions are hard to segment accurately.

## Tomorrow's Plan
* Compare global aggregated Dice vs per-hospital local Dice.
