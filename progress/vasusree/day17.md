# Vasu Sree Day 17 - test(resilience): validate server graceful handling across multi-round dropout

## Tasks Completed
* Hospital-B offline for Rounds 3-7; back online for Rounds 8-10.
* Server: Rounds 3-7 complete with 2 clients; Rounds 8-10 complete with all 3 clients.
* Final Dice: 0.681 (2 clients dropped) vs 0.693 (all clients) — 1.2% performance cost of dropout.

## Files Modified/Created
* `results/resilience_test_results.json` — multi-round dropout results

## Notes & Challenges
* 1.2% Dice loss due to 5 rounds without Hospital-B is acceptable; validates fault tolerance.

## Tomorrow's Plan
* Add automatic client reconnection with exponential backoff.
