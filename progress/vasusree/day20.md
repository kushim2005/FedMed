# Vasu Sree Day 20 - feat(client): implement client-side file logging

## Tasks Completed
* Added `_setup_file_logging()` in `HospitalClientV2`: creates `logs/hospital_{id}.log`.
* Per-round entries: timestamp, round number, loss, Dice, epoch details.
* Log rotation: `RotatingFileHandler(maxBytes=10MB, backupCount=3)`.

## Files Modified/Created
* `client/fl_client_v2.py` — `_setup_file_logging()` method (25 lines)
* `logs/` — directory created by client at startup

## Notes & Challenges
* Log files are volume-mounted in Docker: `./logs:/app/logs` for host access.

## Tomorrow's Plan
* Full Docker TLS simulation: 3 hospitals × 10 FL rounds.
