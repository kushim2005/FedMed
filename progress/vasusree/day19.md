# Vasu Sree Day 19 - feat(docker): add CPU/RAM resource limits per hospital container

## Tasks Completed
* Added `deploy.resources.limits: cpus: "2.0", memory: 4G` to each hospital in docker-compose.yml.
* Tested: all 3 hospitals run within limits; no OOM kills in 10-round simulation.
* Server container: 4 CPUs, 8 GB RAM (aggregation needs more memory).

## Files Modified/Created
* `docker-compose.yml` — resource limits for all 4 services

## Notes & Challenges
* Docker resource limits require `docker-compose` v3.7+; confirmed version compatibility.

## Tomorrow's Plan
* Implement client-side file logging to `logs/hospital_{id}.log`.
