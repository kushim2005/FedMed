# Day 33 — Sept 28 | Chaitanya | ML Research

## Focus: DP Noise Analysis + Accuracy Trade-off

### Tasks Completed
- Implemented DP noise impact analysis: swept sigma from 0.5 to 2.0
- Results: sigma=1.1 gives best accuracy-privacy trade-off at epsilon≈2.8
- Confirmed Dice degrades gracefully: 0.691 → 0.683 with sigma=1.1 (target 0.68 ✓)
- Found optimal clipping norm C=1.0: covers 95% of gradient norms during training
- Tested Opacus PrivacyEngine attachment to FedMed3DUNet: compatible with MONAI
- Measured: DP-SGD epoch time 1.3× slower than SGD (gradient clipping overhead)

### Noise Multiplier Study
| sigma | epsilon (T=10) | Dice  |
|-------|----------------|-------|
| 0.5   | 8.4            | 0.689 |
| 0.8   | 4.2            | 0.687 |
| 1.1   | 2.8            | 0.683 |
| 1.5   | 1.9            | 0.671 |
| 2.0   | 1.4            | 0.652 |

### Tomorrow
- Integrate DP noise analysis into docs/week4_pipeline.md
- Review fl_client_dp.py from Kushi
