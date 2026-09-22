# Kushi Day 27 - test(server): write unit tests for server aggregation logic

## Tasks Completed
* Created `tests/test_server.py` with 4 unit tests.
* Tests: `weighted_average()` correctness, `build_strategy()` returns correct type, server config validation.
* All 4 tests pass: `pytest tests/test_server.py -v`.

## Files Modified/Created
* `tests/test_server.py` — 4 unit tests (60 lines)

## Notes & Challenges
* Mocked Flower `Parameters` object to test aggregation without full FL loop.

## Tomorrow's Plan
* Week 2 FL server complete — final commit and merge.
