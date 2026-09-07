# Kushi Day 12 - fix(server): debug TLS server startup and cert path resolution

## Tasks Completed
* Fixed: cert paths were relative; switched to `Path(__file__).parent / "certs"` for absolute resolution.
* Server now starts cleanly with TLS: `INFO: FL Server listening on 0.0.0.0:8080 [TLS]`.
* Tested with `openssl s_client -connect localhost:8080` — handshake succeeds.

## Files Modified/Created
* `security/tls_config.py` — absolute path fix
* `server/fl_server_v2.py` — startup logging improvements

## Notes & Challenges
* Flower 1.6 expects `(ca_cert_bytes, [(server_key_bytes, server_cert_bytes)])` format.

## Tomorrow's Plan
* Add FedAvg strategy alongside FedProx; make strategy configurable via YAML.
