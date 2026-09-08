# Kushi Day 13 - feat(server): add configurable FedAvg + FedProx strategy selection

## Tasks Completed
* Created `FedMedAggregateStrategy` subclass extending `fl.server.strategy.FedProx`.
* Added `strategy: "fedprox"` vs `"fedavg"` option in `config/week2_config.yaml`.
* Confirmed FedProx with `proximal_mu=0.1` is default; FedAvg available for comparison.

## Files Modified/Created
* `server/fl_server_v2.py` — strategy factory `build_strategy(config)` added

## Notes & Challenges
* FedProx is a superset of FedAvg (mu=0 reduces to FedAvg); kept as single class.

## Tomorrow's Plan
* Implement `min_available_clients=2` for client dropout tolerance.
