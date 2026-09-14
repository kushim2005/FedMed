# Ravi Day 19 - feat(demo): start demo/week2_demo.py orchestration script

## Tasks Completed
* Created `demo/week2_demo.py` skeleton: generates certs, partitions data, starts server + 3 clients.
* Added CLI args: `--data-dir`, `--num-rounds`, `--no-tls`, `--alpha`.
* Tested dry-run (no-tls mode) with mock data — server and clients launch successfully.

## Files Modified/Created
* `demo/week2_demo.py` — 120-line orchestration script

## Notes & Challenges
* Need to integrate Vasu Sree's Docker-based demo path for production use.

## Tomorrow's Plan
* Integrate TLS cert paths into demo script configuration.
