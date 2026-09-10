# Chaitanya Day 15 - Implement model checkpointing for best global model

## Tasks Completed
* Added `save_checkpoint()` in `train/federated_train.py` using `torch.save()`
* Checkpoint saves global model state_dict when val Dice exceeds previous best
* Best model persisted to `checkpoints/global_best.pth` after each FL round

## Files Modified/Created
* `train/federated_train.py` - `save_checkpoint()` and `load_checkpoint()` added
* `checkpoints/` - directory initialized; `global_best.pth` written after round 5

## Notes & Challenges
* Had to track `best_dice` in server aggregation loop; passed via Flower metrics dict

## Tomorrow's Plan
* Add per-client early stopping with patience=3 rounds
