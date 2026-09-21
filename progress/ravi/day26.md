# Ravi Day 26 - fix(data): adjust Dirichlet alpha after mid-project review feedback

## Tasks Completed
* Mentor feedback: alpha=0.5 causes Hospital-C to have only 30% of Hospital-A data.
* Changed default from alpha=0.5 to alpha=0.8 in `config/week2_config.yaml`.
* Re-ran partitioning: Hospital-A=136, Hospital-B=120, Hospital-C=113 (more balanced).

## Files Modified/Created
* `config/week2_config.yaml` — `dirichlet_alpha: 0.8`
* `data/partition.py` — updated docstring with alpha guidelines

## Notes & Challenges
* Will keep alpha=0.5 available as a CLI option for heterogeneity experiments in Week 3.

## Tomorrow's Plan
* Final integration pass and cleanup.
