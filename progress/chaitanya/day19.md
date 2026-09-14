# Chaitanya Day 19 - Implement FedProx proximal loss term

## Tasks Completed
* Added proximal term `(mu/2) * ||w_local - w_global||^2` to client loss in `train_one_epoch()`
* Set `mu=0.01` as default in `config/week2_config.yaml`
* Cloned global weights at round start; proximal penalty computed per batch

## Files Modified/Created
* `train/federated_train.py` - proximal loss term added to total loss computation
* `config/week2_config.yaml` - added `fedprox_mu: 0.01`
* `client/fl_client_v2.py` - global weights snapshot passed into train call

## Notes & Challenges
* Must deep-copy global weights before local updates; reference copy caused silent bug

## Tomorrow's Plan
* Compare FedProx vs FedAvg val Dice across 5 FL rounds
