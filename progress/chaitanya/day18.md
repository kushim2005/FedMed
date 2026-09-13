# Chaitanya Day 18 - Gradient accumulation steps=4 to handle memory constraints

## Tasks Completed
* Refactored `train_one_epoch()` to accumulate gradients over 4 mini-batches
* Divided loss by `accumulation_steps` before backward; `optimizer.step()` every 4th step
* Verified peak VRAM dropped to 4.8 GB with effective batch size unchanged

## Files Modified/Created
* `train/federated_train.py` - gradient accumulation loop with `accumulation_steps=4`
* `config/week2_config.yaml` - added `grad_accum_steps: 4`

## Notes & Challenges
* GradScaler needed adjustment: `scaler.update()` only called on accumulation boundary

## Tomorrow's Plan
* Implement FedProx proximal loss term for non-IID robustness
