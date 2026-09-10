# Kushi Day 15 - feat(server): add per-round logging and metrics tracking

## Tasks Completed
* Overrode `aggregate_evaluate()` in `FedMedAggregateStrategy` to log per-round Dice.
* Logs: `Round 3 | Global Dice: 0.6241 | Clients: 3`.
* Metrics list saved to `results/server_round_metrics.json` after each round.

## Files Modified/Created
* `server/fl_server_v2.py` — `aggregate_evaluate()` override with logging

## Notes & Challenges
* `aggregate_evaluate` receives `(loss, metrics)` from Flower; metrics include `dice_score` key.

## Tomorrow's Plan
* Add global model checkpoint saving every 5 rounds.
