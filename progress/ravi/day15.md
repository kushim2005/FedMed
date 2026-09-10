# Ravi Day 15 - test(connectivity): review TLS setup and verify server on port 8080

## Tasks Completed
* Reviewed Kushi's `security/tls_config.py` and `security/generate_certs.py`.
* Ran `python security/generate_certs.py` — CA, server, and 3 client certs generated in `security/certs/`.
* Verified server starts on port 8080 with TLS: `openssl s_client -connect localhost:8080`.

## Files Modified/Created
* `security/certs/` — 9 cert/key files generated

## Notes & Challenges
* `openssl s_client` test confirmed TLS handshake works with self-signed CA.

## Tomorrow's Plan
* Implement end-to-end FL simulation orchestration script.
