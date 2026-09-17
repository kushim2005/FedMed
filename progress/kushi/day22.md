# Kushi Day 22 - docs(review): mid-project review — server demo and TLS documentation

## Tasks Completed
* Prepared live server demo: `python server/fl_server_v2.py --config config/week2_config.yaml`.
* Documented TLS setup procedure in `docs/week2_pipeline.md` (cert generation → server start → client connect).
* Presented server metrics to team: 10-round convergence confirmed.

## Files Modified/Created
* `docs/week2_pipeline.md` — TLS server architecture section (50 lines)

## Notes & Challenges
* Team requested adding `--strategy` CLI flag to easily switch FedProx/FedAvg.

## Tomorrow's Plan
* Document complete gRPC TLS architecture in `docs/week2_pipeline.md`.
