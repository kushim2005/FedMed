# Chaitanya Day 10 - Implement gradient clipping in train step

## Tasks Completed
* Added `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)` before optimizer.step()
* Confirmed grad norm logs stay ≤1.0 across all batches in test run
* Moved clipping call to correct position after loss.backward() in train loop

## Files Modified/Created
* `train/federated_train.py` - gradient clipping added to `train_one_epoch()`

## Notes & Challenges
* Initially placed clip call after optimizer.step() — caught and fixed; no effect otherwise

## Tomorrow's Plan
* Implement proper 80/20 train/val split per hospital partition
