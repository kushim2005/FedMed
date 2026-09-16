# Vasu Sree Day 21 - test(e2e): full Docker TLS simulation — 3 hospitals × 10 FL rounds

## Tasks Completed
* `docker-compose up --build` — all 4 containers started with health checks passing.
* 10 FL rounds completed in 38 minutes (TLS overhead: ~2% vs non-TLS).
* All log files created: `logs/hospital_1.log`, `logs/hospital_2.log`, `logs/hospital_3.log`.

## Files Modified/Created
* `results/docker_simulation_10_rounds.txt` — timing and round-by-round summary

## Notes & Challenges
* TLS adds ~2% overhead vs non-TLS — negligible for production use.

## Tomorrow's Plan
* Mid-project DevOps review — Docker performance analysis.
