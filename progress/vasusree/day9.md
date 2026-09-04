# Vasu Sree Day 9 - feat(security): implement security/generate_certs.py for all containers

## Tasks Completed
* Co-developed `security/generate_certs.py` with Kushi: generates CA + server + 3 client certs.
* Verified all 9 files generated in `security/certs/`: `ca.crt`, `server.key/crt`, `client_1-3.key/crt`.
* Ran generation script: `python security/generate_certs.py` — completes in 0.8 seconds.

## Files Modified/Created
* `security/generate_certs.py` — complete cert generation (co-authored with Kushi)
* `security/certs/` — 9 PEM files generated

## Notes & Challenges
* Each hospital container gets its own client cert (`client_{id}.key/crt`) for mutual identification.

## Tomorrow's Plan
* Update Dockerfile to copy TLS certs into hospital image.
