# Kushi Day 9 - feat(security): create security/generate_certs.py for TLS certificate generation

## Tasks Completed
* Implemented `generate_ca_cert()` — self-signed 10-year CA cert using RSA-2048.
* Implemented `generate_signed_cert(ca_key, ca_cert, common_name)` for server and client certs.
* Implemented `save_cert(name, key, cert)` — saves `.key` and `.crt` PEM files to `security/certs/`.

## Files Modified/Created
* `security/__init__.py` — package init
* `security/generate_certs.py` — full cert generation script (120 lines)

## Notes & Challenges
* Used `x509.SubjectAlternativeName` with `DNSName("localhost")` for local dev TLS.

## Tomorrow's Plan
* Create `security/tls_config.py` — cert loading utilities for gRPC.
