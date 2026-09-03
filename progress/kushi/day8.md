# Kushi Day 8 - research(security): study Flower TLS/SSL and gRPC certificate requirements

## Tasks Completed
* Read Flower 1.6 docs on gRPC SSL: `fl.server.start_server(certificates=...)` accepts `grpc.ServerCredentials`.
* Studied `cryptography` library for Python-native cert generation (no openssl binary needed).
* Outlined cert hierarchy: Root CA → Server Cert → 3 Client Certs.

## Files Modified/Created
* `docs/week2_pipeline.md` — TLS architecture section (draft)

## Notes & Challenges
* Flower TLS requires passing `(private_key_bytes, cert_chain_bytes)` tuples, not file paths.

## Tomorrow's Plan
* Create `security/generate_certs.py` — CA + server cert generation.
