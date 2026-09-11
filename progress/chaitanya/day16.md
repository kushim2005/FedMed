# Chaitanya Day 16 - Add early stopping per client (patience=3)

## Tasks Completed
* Implemented `EarlyStopping` class in `train/federated_train.py` with `patience=3`
* Client skips local training round if val Dice has not improved for 3 consecutive rounds
* Tested: Hospital-B client stopped at round 7 as expected in a dry run

## Files Modified/Created
* `train/federated_train.py` - `EarlyStopping` class added, wired into `fl_client_v2.py`
* `client/fl_client_v2.py` - early stopping hook called before `fit()` returns

## Notes & Challenges
* Server must still aggregate even if some clients skip; handled via sample-weighted FedAvg

## Tomorrow's Plan
* Profile GPU memory usage with 3D UNet on 128³ patches
