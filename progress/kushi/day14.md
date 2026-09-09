# Kushi Day 14 - feat(server): implement client dropout tolerance (min_available_clients=2)

## Tasks Completed
* Set `min_available_clients=2` in strategy — server waits for 2/3 hospitals max.
* Tested: killed Hospital-C mid-wait; server proceeded with Hospital-A and Hospital-B.
* Round still completes with 2 clients; global weights aggregated from 2 updates.

## Files Modified/Created
* `server/fl_server_v2.py` — `min_fit_clients=2`, `min_available_clients=2`
* `config/week2_config.yaml` — `min_clients: 2`

## Notes & Challenges
* With `min_clients=2`, one hospital can go offline without aborting the FL round.

## Tomorrow's Plan
* Add per-round server-side logging (round number, client count, avg Dice).
