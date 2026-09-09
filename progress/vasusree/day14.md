# Vasu Sree Day 14 - test(client): TLS handshake test — Hospital-A container to server

## Tasks Completed
* End-to-end TLS test: `docker-compose up fl_server hospital_1` — Round 1 completes.
* Hospital-A (AIIMS) log: `Connected to fl_server:8080 [TLS] | Round 1 | Loss: 0.8821`.
* Server log: `Round 1 | 1 client | Dice: 0.5412` — correct single-client aggregation.

## Files Modified/Created
* `logs/hospital_1.log` — file logging working correctly

## Notes & Challenges
* Single-client run triggers `min_clients=2` wait; tested with `min_clients=1` override for this test.

## Tomorrow's Plan
* Add Docker health checks to Dockerfile.
