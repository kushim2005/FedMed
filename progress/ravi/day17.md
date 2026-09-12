# Ravi Day 17 - fix(data): resolve num_workers DataLoader bottleneck

## Tasks Completed
* Profiled DataLoader with `num_workers=4` vs `num_workers=2` vs `num_workers=0`.
* Windows multiprocessing with `num_workers>2` causes inter-process conflicts.
* Set `num_workers=2` as default in `config/week2_config.yaml`; documented reason.

## Files Modified/Created
* `config/week2_config.yaml` — `num_workers: 2`
* `data/dataset.py` — added Windows-specific warning in docstring

## Notes & Challenges
* On Linux/Mac `num_workers=4` is fine; this is Windows-only quirk.

## Tomorrow's Plan
* Validate non-IID distribution statistics using matplotlib histograms.
