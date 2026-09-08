# Ravi Day 13 - test(integration): validate partitioned data loading in fl_client_v2

## Tasks Completed
* Tested loading Hospital-A partition (147 cases) via `get_dataloaders()`.
* Confirmed MONAI transforms pipeline handles partitioned indices correctly.
* Fixed: `hospital_id` was not being passed to `get_dataloaders()` — patched in `data/dataset.py`.

## Files Modified/Created
* `data/dataset.py` — added `partition_indices` parameter to `get_dataloaders()`

## Notes & Challenges
* DataLoader `num_workers=4` caused deadlock on Windows — reduced to 2.

## Tomorrow's Plan
* Write unit tests for `partition.py` in `tests/test_partition.py`.
