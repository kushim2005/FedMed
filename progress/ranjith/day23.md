# Ranjith Day 23 - feat(eval): generate per-hospital confusion matrices

## Tasks Completed
* Generated confusion matrices for NCR/ED/ET classification per hospital.
* Saved `results/confusion_matrix_hospital_{1,2,3}.png` using seaborn heatmaps.
* Hospital-C shows highest ET false-negative rate (smaller ET regions in its partition).

## Files Modified/Created
* `eval/confusion_matrix.py` — confusion matrix generator (60 lines)
* `results/confusion_matrix_hospital_*.png` — 3 heatmaps

## Notes & Challenges
* 4-class confusion matrix (Background + NCR + ED + ET) requires flattening 3D predictions.

## Tomorrow's Plan
* Write `eval/README.md` documenting the FederatedMetricsTracker API.
