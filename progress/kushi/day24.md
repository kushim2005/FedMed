# Kushi Day 24 - analysis(server): FedProx vs FedAvg convergence comparison

## Tasks Completed
* Ran 10 rounds each with FedProx (mu=0.1) and FedAvg on same non-IID partitions (alpha=0.5).
* FedProx: Round 10 Dice = 0.693 | FedAvg: Round 10 Dice = 0.671 — FedProx +3.2% advantage.
* Saved comparison to `results/fedprox_vs_fedavg_comparison.json`.

## Files Modified/Created
* `results/fedprox_vs_fedavg_comparison.json` — strategy comparison

## Notes & Challenges
* FedProx advantage larger with non-IID (alpha=0.5); expected to shrink with alpha=0.8.

## Tomorrow's Plan
* Add configurable `num_rounds` and `strategy` to YAML config.
