# Ravi Day 21 - test(e2e): full end-to-end test — 3 hospitals, 5 FL rounds

## Tasks Completed
* Ran complete FL simulation: 3 hospitals x 5 rounds with TLS enabled.
* All 5 rounds completed successfully; global Dice improved from 0.54 → 0.62.
* Server saved checkpoint at round 5 to `checkpoints/global_model_round_5.pt`.

## Files Modified/Created
* `results/server_round_metrics.json` — 5-round metrics output

## Notes & Challenges
* Round 3 took 8.2 min (Hospital-C had more data); acceptable for full BraTS.

## Tomorrow's Plan
* Mid-project review prep — generate data validation report.
