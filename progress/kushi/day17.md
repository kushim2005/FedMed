# Kushi Day 17 - test(server): 3-client TLS handshake test with mock hospital clients

## Tasks Completed
* Launched server + 3 Hospital clients (mock data, 1 local epoch each).
* All 3 TLS handshakes confirmed: `SSL_connect: ok` in client logs.
* Round 1 completed: 3 hospitals aggregated, global Dice = 0.5841.

## Files Modified/Created
* `tests/test_tls_handshake.py` — automated TLS connectivity test

## Notes & Challenges
* Hospital-B client cert CN must match `hospital-2` exactly; fixed typo in `generate_certs.py`.

## Tomorrow's Plan
* Fine-tune FedProx proximal term mu; compare mu=0.1 vs mu=0.01.
