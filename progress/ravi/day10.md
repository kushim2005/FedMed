# Ravi Day 10 - feat(data): complete partition_brats_dataset() with JSON index output

## Tasks Completed
* Implemented `partition_brats_dataset(data_dir, num_clients, alpha)` function.
* Function discovers BraTS case directories, partitions indices, saves `partition_map_alpha0.5_n3.json`.
* Added `load_partition_map()` utility for reproducible loading.

## Files Modified/Created
* `data/partition.py` — complete implementation (130 lines)

## Notes & Challenges
* BraTS directory discovery uses `sorted([d for d in path.iterdir() if d.is_dir()])`.

## Tomorrow's Plan
* Test partitioning on actual BraTS dataset, fix any edge cases.
