# Day 28 — Sept 23 | Ranjith Kumar | ML Engineering

## Focus: Week 2 Wrap-Up + Week 3 Test Infrastructure Planning

### Tasks Completed
- Finalized Week 2 metrics export: CSV with per-round Dice, Loss, HD95 for all 10 rounds
- Verified eval/federated_metrics.py flake8 clean (F841 fix confirmed in CI)
- Week 3 test infrastructure planning:
  - Defined test cases for HE encryption module (to be implemented Day 29)
  - Researched pytest-mock approach for TenSEAL ciphertext mocking
  - Designed test isolation: TenSEAL optional dependency (skip if not installed)
  - Wrote test plan document for encryption/tests/
- Reviewed CI pipeline: confirmed flake8 passes on all Week 2 files
- Set up Week 3 branch structure: `feature/week3-he-encryption`

### Week 2 Metrics Final Export (Round 10)
```
round,dice,dice_et,dice_ed,dice_ncr,hd95,loss
10,0.712,0.710,0.740,0.580,12.4,0.142
```

### Week 3 Test Plan
1. test_context_creation — CKKS params validation
2. test_encrypt_decrypt_roundtrip — L2 error < 1e-4
3. test_aggregation_correctness — weighted avg of 3 ciphertexts
4. test_key_serialization — save/load round-trip
5. test_edge_cases — zero/near-zero/large values

### Tomorrow
- Begin tests/test_he_encryption.py scaffolding
