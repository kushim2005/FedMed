# Ranjith Day 14 - test(eval): validate FedAvg weighted average correctness

## Tasks Completed
* Wrote `tests/test_fedavg_math.py`: given 3 clients with known weights and sample counts, verify `weighted_average()` output matches manual calculation.
* Test passes: weighted Dice = (147*0.65 + 112*0.61 + 110*0.72) / 369 = 0.6596 ✓.
* Confirmed Flower's FedAvg uses sample-count weighting (not uniform averaging).

## Files Modified/Created
* `tests/test_fedavg_math.py` — 3 unit tests (40 lines)

## Notes & Challenges
* Floating-point precision: used `assertAlmostEqual(result, expected, places=4)`.

## Tomorrow's Plan
* Statistical comparison: non-IID vs IID partitioning effect on Dice convergence.
