# Ravi Day 16 - feat(train): implement end-to-end FL simulation script skeleton

## Tasks Completed
* Reviewed `train/federated_train.py` from Chaitanya, added `subprocess.Popen` orchestration.
* Server launches first (3s sleep), then 3 hospital clients sequentially.
* Added stdout streaming for real-time FL round progress.

## Files Modified/Created
* `train/federated_train.py` — orchestration logic (added process management)

## Notes & Challenges
* 3-second wait after server start is not robust; TODO: add server readiness probe.

## Tomorrow's Plan
* Debug `num_workers` DataLoader bottleneck — currently slow on Windows.
