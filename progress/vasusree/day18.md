# Vasu Sree Day 18 - feat(client): add exponential backoff reconnection to fl_client_v2.py

## Tasks Completed
* Implemented retry loop in `start_client()`: max 5 retries, delay doubles each attempt (2→4→8→16→32s).
* If Hospital-B goes down and comes back, it reconnects at next available round.
* Tested: Hospital-B stopped for 45s, restarted — reconnected at Round 6.

## Files Modified/Created
* `client/fl_client_v2.py` — exponential backoff (20 lines added)

## Notes & Challenges
* Flower client reconnects by calling `start_numpy_client()` again — stateless reconnect.

## Tomorrow's Plan
* Add Docker resource limits (2 CPU, 4 GB RAM) per hospital container.
