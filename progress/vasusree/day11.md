# Vasu Sree Day 11 - feat(docker): update docker-compose.yml with TLS volumes and network

## Tasks Completed
* Added `./security/certs:/app/security/certs:ro` volume mount to all 3 hospital services.
* Added `fl_network` bridge network; all containers on same network for DNS resolution.
* Added TLS env vars: `FL_SERVER_HOST=fl_server`, `USE_TLS=true`, `HOSPITAL_ID=1/2/3`.

## Files Modified/Created
* `docker-compose.yml` — TLS volumes + fl_network + env vars (rewritten, 60 lines)

## Notes & Challenges
* `fl_server` container name is used as DNS hostname for hospital clients.

## Tomorrow's Plan
* Test TLS Docker container-to-container connectivity.
