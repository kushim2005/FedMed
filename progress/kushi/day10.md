# Kushi Day 10 - feat(security): create security/tls_config.py with gRPC credential loaders

## Tasks Completed
* Implemented `load_server_credentials()` → returns `grpc.ssl_server_credentials()`.
* Implemented `load_client_credentials(hospital_id)` → returns `grpc.ssl_channel_credentials()`.
* Added `certs_exist()` utility to validate all 9 required cert/key files are present.

## Files Modified/Created
* `security/tls_config.py` — TLS utilities (70 lines)

## Notes & Challenges
* `grpc.ssl_server_credentials` requires `require_client_auth=False` for one-way TLS.

## Tomorrow's Plan
* Update `server/fl_server_v2.py` with TLS configuration.
