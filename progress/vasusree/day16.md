# Vasu Sree Day 16 - test(resilience): simulate Hospital-B node failure mid-FL-round

## Tasks Completed
* During Round 3 of 10-round simulation: `docker stop fedmed_hospital_2_1`.
* Server log: `Round 3 | 2/3 clients responded | Proceeding with min_clients=2`.
* Round 3 completes with Hospital-A + Hospital-C; training continues to Round 10.

## Files Modified/Created
* `tests/test_node_resilience.py` — automated failure simulation test

## Notes & Challenges
* Flower server waits up to `timeout` seconds for minimum clients; graceful degradation confirmed.

## Tomorrow's Plan
* Test full server handling of client dropout across all rounds.
