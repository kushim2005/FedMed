# Chaitanya Day 9 - Add CosineAnnealingLR scheduler to local training loop

## Tasks Completed
* Added `torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)` to train loop
* Called `scheduler.step()` after each epoch in `train/federated_train.py`
* Verified LR decays from 1e-3 → ~0 over 10 rounds via debug print

## Files Modified/Created
* `train/federated_train.py` - integrated CosineAnnealingLR, added scheduler.step()

## Notes & Challenges
* Had to ensure scheduler state is not included in FedAvg weight aggregation

## Tomorrow's Plan
* Add gradient clipping to the training step
