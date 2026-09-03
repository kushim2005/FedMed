# Vasu Sree Day 8 - research(devops): research Docker TLS volume mounting strategies

## Tasks Completed
* Researched Docker bind-mount vs named-volume strategies for TLS cert distribution.
* Decided: generate certs on host once; bind-mount `./security/certs` into each container.
* Studied `docker-compose.yml` secrets vs volumes — volumes chosen for simplicity.

## Files Modified/Created
* `docs/week2_pipeline.md` — Docker TLS section (draft)

## Notes & Challenges
* Docker secrets are more secure but require Swarm mode; bind-mount is acceptable for dev.

## Tomorrow's Plan
* Implement `security/generate_certs.py` — CA, server, and 3 client cert generation.
