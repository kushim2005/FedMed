# Chaitanya Day 12 - Integrate AMP GradScaler into federated training loop

## Tasks Completed
* Wrapped forward pass with `torch.cuda.amp.autocast()` in `train_one_epoch()`
* Added `GradScaler` with `scaler.scale(loss).backward()` and `scaler.step(optimizer)`
* Measured ~1.4× epoch speedup on Hospital-A shard (A100 GPU)

## Files Modified/Created
* `train/federated_train.py` - AMP autocast + GradScaler fully integrated
* `config/week2_config.yaml` - added `use_amp: true` flag

## Notes & Challenges
* GradScaler must be instantiated once and passed to client train loop, not recreated per round

## Tomorrow's Plan
* Run 5-epoch local training on Hospital-A partition and record Dice
