# Vasu Sree Day 13 - feat(client): implement client/fl_client_v2.py with TLS support

## Tasks Completed
* Created `client/fl_client_v2.py` extending Week 1 `HospitalClient`.
* Added `grpc.ssl_channel_credentials(root_ca)` for TLS channel.
* Added exponential backoff reconnection: 5 retries, doubling delay (2s → 32s).

## Files Modified/Created
* `client/fl_client_v2.py` — TLS client with reconnection (200 lines)

## Notes & Challenges
* Flower 1.6 `start_numpy_client` accepts `root_certificates` bytes for TLS.

## Tomorrow's Plan
* Test full TLS handshake: Hospital-A container ↔ FL server.
