# Day 34 — Sept 29 | Chaitanya | ML Research

## Focus: DP-SGD Full Training Run + Validation

### Tasks Completed
- Ran full 10-round DP-SGD training with sigma=1.1, C=1.0, delta=1e-5
- Final Dice: 0.683 (target ≥0.68 ✓), epsilon=2.79 (target ≤3.0 ✓)
- Per-class results: ET=0.672, ED=0.715, NCR=0.556, HD95=14.2mm
- Convergence comparison chart: plaintext FedProx vs. HE vs. DP-SGD
  - DP-SGD converges 1-2 rounds slower but reaches comparable final Dice
- Wrote accuracy-vs-privacy table for docs/week4_pipeline.md
- Validated Rényi DP accounting matches theoretical bounds from Mironov 2017

### Final DP-SGD Results
| Metric         | Value  | Target | Status |
|----------------|--------|--------|--------|
| Dice Score     | 0.683  | ≥0.68  | ✅     |
| Epsilon (ε)    | 2.79   | ≤3.0   | ✅     |
| Delta (δ)      | 1e-5   | 1e-5   | ✅     |
| HD95           | 14.2mm | —      | ✅     |

### Tomorrow
- Final review of all Week 4 deliverables
- Help with demo/week4_demo.py testing
