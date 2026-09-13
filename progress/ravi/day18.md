# Ravi Day 18 - analysis(data): validate non-IID distribution statistics

## Tasks Completed
* Generated matplotlib bar charts showing per-hospital case counts for alpha=0.5 and alpha=1.0.
* Confirmed alpha=0.5 produces meaningful heterogeneity (CV=0.14 across hospitals).
* Saved distribution plot to `results/partition_distribution.png`.

## Files Modified/Created
* `scripts/visualize_partition.py` — partition distribution visualizer (40 lines)
* `results/partition_distribution.png` — distribution chart

## Notes & Challenges
* Alpha=0.1 creates extreme imbalance (1 hospital gets 70% of data); decided alpha=0.5 is appropriate.

## Tomorrow's Plan
* Start `demo/week2_demo.py` orchestration script.
