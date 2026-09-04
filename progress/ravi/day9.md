# Ravi Day 9 - feat(data): implement DirichletPartitioner class in data/partition.py

## Tasks Completed
* Implemented `DirichletPartitioner` class with configurable `alpha` and `seed`.
* Added `np.random.default_rng(seed)` for reproducible partitions.
* Verified that proportions sum to 1.0 and no partition is empty.

## Files Modified/Created
* `data/partition.py` — DirichletPartitioner class (90 lines)

## Notes & Challenges
* Edge case: small datasets can produce zero-size partitions with low alpha; added `max(size, 1)` guard.

## Tomorrow's Plan
* Complete `partition_brats_dataset()` function and JSON index saving.
