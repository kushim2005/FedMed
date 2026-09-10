# Vasu Sree Day 15 - feat(docker): add HEALTHCHECK to Dockerfile

## Tasks Completed
* Added `HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8090/health || exit 1`.
* FL server exposes health endpoint on port 8090 (implemented by Kushi).
* `docker ps` now shows `(healthy)` status after 30s for both server and client containers.

## Files Modified/Created
* `Dockerfile` — HEALTHCHECK directive added
* `docker-compose.yml` — `depends_on: condition: service_healthy` for hospital containers

## Notes & Challenges
* `depends_on: service_healthy` ensures hospitals only start once server is healthy.

## Tomorrow's Plan
* Implement node failure simulation: kill Hospital-B mid-round.
