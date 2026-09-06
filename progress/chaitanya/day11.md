# Chaitanya Day 11 - Add 80/20 train/val split per hospital partition

## Tasks Completed
* Updated `get_dataloaders()` in `data/partition.py` to split each hospital shard 80/20
* Used stratified random seed per client ID to ensure reproducibility
* Validated split sizes: Hospital-A 96 train / 24 val from 120 BraTS cases

## Files Modified/Created
* `data/partition.py` - added `train_val_split()` helper, updated `get_dataloaders()`

## Notes & Challenges
* Dirichlet-partitioned shards had unequal sizes; split must be applied per-shard

## Tomorrow's Plan
* Integrate AMP GradScaler into federated training loop
