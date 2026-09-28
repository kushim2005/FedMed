# Day 33 — Sept 28 | Kushi | FL Systems

## Focus: Privacy Budget Implementation

### Tasks Completed
- Implemented `privacy/privacy_budget.py`:
  - `PrivacyBudget` class using Opacus RDP accountant
  - `step(noise_multiplier, sample_rate, steps)`: advances accountant
  - `get_epsilon(delta=1e-5)`: converts RDP to (ε,δ)-DP
  - `is_budget_exceeded(max_epsilon)`: budget enforcement
  - `reset()`: restart accounting (for ablation studies)
- Implemented `client/fl_client_dp.py`:
  - Wraps training loop with Opacus PrivacyEngine
  - `DP_ENABLED` env var controls activation
  - Noise multiplier σ and clip norm C configurable via YAML
  - Reports epsilon to server after each round
- Tested with Chaitanya's sigma=1.1 recommendation: ε=2.79 after 10 rounds ✓

### Privacy Budget Accounting
- Accountant: Rényi DP (RDP) via Opacus
- Conversion: Mironov 2017 RDP → (ε,δ)-DP
- Parameters: σ=1.1, C=1.0, batch_size=2, n=100, T=10 rounds
- Final ε = 2.79, δ = 1e-5 ✓

### Tomorrow
- Integration test fl_client_dp + fl_server + privacy_budget
