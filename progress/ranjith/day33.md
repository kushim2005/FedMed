# Day 33 — Sept 28 | Ranjith Kumar | ML Engineering

## Focus: Privacy-Utility Metrics Framework

### Tasks Completed
- Implemented privacy-utility metrics in `eval/federated_metrics.py`:
  - `log_privacy_round(round_id, epsilon, delta, noise_multiplier, dice)`
  - `get_privacy_summary()`: returns final epsilon, dice at convergence
  - `export_privacy_csv(path)`: exports per-round privacy metrics to CSV
- Added Pareto front analysis: identifies optimal epsilon-Dice pairs
- Wrote `tests/test_privacy_metrics.py`: 4 test cases all passing
- Documented privacy metric schema for dashboard API

### Privacy Metrics Schema
```yaml
privacy_round:
  round_id: int
  epsilon: float          # cumulative Rényi DP epsilon
  delta: float            # fixed 1e-5
  noise_multiplier: float # sigma
  clip_norm: float        # C
  dice_score: float       # model accuracy this round
```

### Tomorrow
- Implement week4 docs and final report
