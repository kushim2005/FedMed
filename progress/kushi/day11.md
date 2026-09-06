# Kushi Day 11 - feat(server): update fl_server_v2.py with TLS gRPC support

## Tasks Completed
* Created `server/fl_server_v2.py` extending Week 1 `fl_server.py`.
* Integrated `load_server_credentials()` into `fl.server.start_server(certificates=...)`.
* Added `--no-tls` CLI flag for local testing without certs.

## Files Modified/Created
* `server/fl_server_v2.py` — TLS-enabled FL server (180 lines)

## Notes & Challenges
* Flower 1.6 passes SSL credentials as a tuple `(root_ca_bytes, [(key, cert)])` — not a `grpc.ServerCredentials` object directly.

## Tomorrow's Plan
* Test TLS server startup, debug cert path issues.
