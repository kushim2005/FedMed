# Ranjith Day 15 - analysis(eval): non-IID vs IID partitioning effect on Dice

## Tasks Completed
* Ran 5 FL rounds with IID (alpha=10.0 ≈ uniform) vs non-IID (alpha=0.5) partitions.
* IID: Round 5 Dice = 0.681 | non-IID: Round 5 Dice = 0.641 — 4.1% gap.
* Confirmed: FedProx reduces this gap vs FedAvg (FedProx non-IID: 0.663, gap = 2.7%).

## Files Modified/Created
* `results/iid_vs_noniid_comparison.json` — comparison results
* `results/iid_vs_noniid.png` — side-by-side convergence plot

## Notes & Challenges
* 4.1% Dice gap validates the need for FedProx over plain FedAvg on non-IID data.

## Tomorrow's Plan
* Add moving average smoothing (window=3) to all loss curves.
