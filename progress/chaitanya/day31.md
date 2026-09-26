# Day 31 — Sept 26 | Chaitanya | ML Research

## Focus: HE Performance Profiling and Accuracy Analysis

### Tasks Completed
- Full end-to-end profiling of HE-enabled FL round vs. plaintext FL round
- Measured Dice score impact: plaintext 0.706 → HE-enabled 0.694 (1.2% drop from approximation error)
- Analysis confirmed CKKS approximation error does not exceed gradient noise floor
- Produced latency breakdown chart: 55% aggregation, 30% encryption, 15% network
- Wrote performance report for docs/week3_pipeline.md (handoff to Ranjith)
- Fixed edge case: very small weight values near float16 underflow → clamping threshold 1e-6

### Results
| Metric        | Plaintext FL | HE-Enabled FL |
|---------------|-------------|---------------|
| Dice (ET)     | 0.710       | 0.698         |
| Dice (ED)     | 0.740       | 0.726         |
| Dice (NCR)    | 0.580       | 0.569         |
| Round Time    | 8.2s        | 18.6s         |
| Security      | None        | CKKS-128-bit  |

### Tomorrow
- Start DP noise analysis for Week 4 transition
