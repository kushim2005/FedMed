# Kushi Day 16 - feat(server): add global model checkpoint saving every N rounds

## Tasks Completed
* Implemented `_save_checkpoint(server_round, parameters)` in `FedMedAggregateStrategy`.
* Saves `checkpoints/global_model_round_{N}.pt` every 5 rounds.
* Checkpoint includes full model `state_dict` reconstructed from Flower `Parameters`.

## Files Modified/Created
* `server/fl_server_v2.py` — `_save_checkpoint()` method (25 lines)
* `checkpoints/` — directory created automatically

## Notes & Challenges
* Flower `Parameters.tensors` are `bytes` objects; must decode via `np.frombuffer`.

## Tomorrow's Plan
* Test with 3 mock clients — confirm 3-client TLS handshake succeeds.
