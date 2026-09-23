# Day 28 — Sept 23 | Chaitanya | ML Research

## Focus: Week 2 → Week 3 Transition | Homomorphic Encryption Kickoff

### Tasks Completed
- Completed Week 2 final accuracy benchmarks:
  - FedProx Round 10 Dice: 0.712 (ET=0.710, ED=0.740, NCR=0.580)
  - Confirmed Week 2 targets met — TLS + FedProx pipeline stable
- Week 3 kickoff: studied CKKS (Cheon-Kim-Kim-Song) homomorphic encryption scheme
  - Reviewed original CKKS paper: approximate arithmetic for encrypted floats
  - Identified key parameters: poly_mod_degree, coeff_mod_bit_sizes, global_scale
  - Compared TenSEAL vs. PySEAL vs. HEAAN for Python-friendly FL integration
  - Selected TenSEAL 0.3.14 as implementation library
- Documented HE feasibility analysis: CKKS supports float-valued weight encryption
- Shared HE study notes with Kushi for context design starting tomorrow

### Week 2 Final Summary
| Metric    | Value  |
|-----------|--------|
| Dice (overall) | 0.712 |
| Dice (ET) | 0.710 |
| Dice (ED) | 0.740 |
| Dice (NCR)| 0.580 |
| HD95      | 12.4mm |
| Rounds    | 10     |
| Clients   | 3      |

### Week 3 Plan
- Day 29–30: HE library benchmarking + gradient compatibility layer
- Day 31–32: Full profiling and accuracy-security trade-off analysis

### Tomorrow
- Benchmark TenSEAL encryption latency on FedMed 3D U-Net weight vectors
