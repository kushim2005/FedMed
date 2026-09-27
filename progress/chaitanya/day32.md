# Day 32 — Sept 27 | Chaitanya | ML Research

## Focus: HE Integration Finalized + DP Preparation

### Tasks Completed
- Validated HE aggregation correctness: server decrypt(aggregate(ciphertexts)) == plaintext_aggregate (within 1e-4)
- Profiled 10-round HE training: total wall time 186s vs. 82s plaintext (2.27× overhead)
- Confirmed security guarantee: 128-bit security level, polynomial degree n=8192
- Prepared HE overhead vs. security level trade-off table for docs
- Started reading Opacus DP-SGD paper and codebase for Week 4 preparation
- Reviewed Rényi DP accounting mechanism for epsilon calculation

### HE Training Summary (10 rounds)
- Final Dice: 0.691 (target was 0.69 ✓)
- Max CKKS approximation error: 3.2e-5
- No convergence issues observed
- Security: IND-CPA secure under RLWE assumption

### Week 4 Prep
- DP noise multiplier analysis: σ=1.1 gives ε≈2.8 at δ=1e-5 (T=10 rounds, n=100 samples)
- Shared analysis with Kushi and Ranjith for budget tracker implementation
