# Vasu Sree Day 12 - test(docker): validate TLS container-to-container connectivity

## Tasks Completed
* Ran `docker-compose up fl_server hospital_1` — TLS handshake successful.
* Confirmed `hospital_1` logs: `SSL_connect: ok | Server: fl_server:8080`.
* All 3 hospital containers can reach `fl_server:8080` over TLS within `fl_network`.

## Files Modified/Created
* `docker-compose.yml` — minor DNS fix (`server_name: fl-server`)

## Notes & Challenges
* CN in server cert must be `fl-server` (hyphen not underscore) to match Docker service name.

## Tomorrow's Plan
* Implement `client/fl_client_v2.py` with TLS channel credentials.
