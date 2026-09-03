# Ravi Day 8 - feat(data): research Dirichlet non-IID partitioning strategy

## Tasks Completed
* Studied Dirichlet distribution partitioning for federated non-IID simulation.
* Reviewed Week 1 `data/dataset.py` to understand current data loading structure.
* Planned `data/partition.py` API: `DirichletPartitioner` class + `partition_brats_dataset()`.

## Files Modified/Created
* `docs/week2_pipeline.md` — added Week 2 data partitioning section (draft)

## Notes & Challenges
* Lower alpha (e.g., 0.1) creates very imbalanced partitions; alpha=0.5 is a good starting point.

## Tomorrow's Plan
* Start implementing `data/partition.py` — `DirichletPartitioner` class.
