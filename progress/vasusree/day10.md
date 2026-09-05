# Vasu Sree Day 10 - feat(docker): update Dockerfile to include TLS cert mounting

## Tasks Completed
* Added `ENV CERT_DIR=/app/security/certs` to Dockerfile.
* Used bind-mount approach (not COPY) so cert rotation doesn't require image rebuild.
* Updated `CMD` to read cert paths from `CERT_DIR` env var.

## Files Modified/Created
* `Dockerfile` — `CERT_DIR` env var + `.dockerignore` update

## Notes & Challenges
* Bind-mount preferred over `COPY security/certs/` to allow cert rotation without rebuild.

## Tomorrow's Plan
* Update `docker-compose.yml` with cert volumes and TLS environment variables.
