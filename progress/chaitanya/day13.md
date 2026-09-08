# Chaitanya Day 13 - Run 5-epoch local training on Hospital-A partition

## Tasks Completed
* Executed local training on Hospital-A: 96 train / 24 val cases (BraTS subset)
* Achieved val Dice=0.64 after 5 epochs with scheduler + clipping + AMP
* Logged per-epoch loss and Dice to `results/hospital_a_local_run.csv`

## Files Modified/Created
* `train/federated_train.py` - confirmed local-only training mode flag works
* `results/hospital_a_local_run.csv` - created with epoch-level metrics

## Notes & Challenges
* Epoch 4-5 Dice gains were marginal (0.635 → 0.64); scheduler may need tuning

## Tomorrow's Plan
* Compare local Dice=0.64 vs global federated Dice after 5 FL rounds
