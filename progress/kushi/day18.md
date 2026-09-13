# Kushi Day 18 - analysis(server): FedProx proximal term tuning (mu=0.1 vs mu=0.01)

## Tasks Completed
* Ran 5 FL rounds with mu=0.1 and mu=0.01 (separate runs).
* mu=0.1: final Dice = 0.69 | mu=0.01: final Dice = 0.67 — mu=0.1 is better for non-IID.
* Committed mu=0.1 as default in `config/week2_config.yaml`.

## Files Modified/Created
* `config/week2_config.yaml` — `proximal_mu: 0.1`
* `results/fedprox_mu_comparison.json` — comparison results

## Notes & Challenges
* Higher mu constrains local models more strongly; beneficial for heterogeneous data.

## Tomorrow's Plan
* Add server health-check ping endpoint via threading.
