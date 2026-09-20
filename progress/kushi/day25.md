# Kushi Day 25 - feat(server): make num_rounds and strategy fully configurable via YAML

## Tasks Completed
* Updated `build_strategy(config)` to read `strategy: fedprox` or `strategy: fedavg` from YAML.
* Added `--rounds` CLI override: `python fl_server_v2.py --rounds 20`.
* Tested: switching strategy via YAML works without code changes.

## Files Modified/Created
* `server/fl_server_v2.py` — strategy factory updated
* `config/week2_config.yaml` — `strategy: fedprox` field added

## Notes & Challenges
* FedAvg in Flower 1.6 is `fl.server.strategy.FedAvg`; imported and wired up cleanly.

## Tomorrow's Plan
* Final server code review — add docstrings and clean up.
