# Ravi Day 20 - feat(demo): integrate TLS certificate paths into demo/week2_demo.py

## Tasks Completed
* Updated `demo/week2_demo.py` to auto-generate certs if `security/certs/` is empty.
* Added cert validation step: verifies all 9 cert/key files exist before launching server.
* Full TLS demo run: 3 hospitals, 3 FL rounds — successful end-to-end.

## Files Modified/Created
* `demo/week2_demo.py` — TLS integration (140 lines)

## Notes & Challenges
* Auto-generate certs require `cryptography` package; added install check.

## Tomorrow's Plan
* Full end-to-end test: 3 hospitals, 5 FL rounds, all rounds completing.
