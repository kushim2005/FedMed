# Day 29 — Sept 24 | Chaitanya | ML Research

## Focus: Homomorphic Encryption Feasibility Study

### Tasks Completed
- Surveyed CKKS (Cheon-Kim-Kim-Song) scheme papers for approximate HE
- Benchmarked TenSEAL encrypt/decrypt latency on float32 model weight vectors
- Mapped 3D U-Net layer shapes to CKKS slot requirements
- Proposed gradient-compatibility layer: flatten → encrypt → transmit → decrypt → unflatten
- Documented HE overhead analysis: ~2.3× slowdown vs. plaintext aggregation
- Shared benchmark results with Kushi for server-side aggregation tuning

### Metrics Observed
- CKKS encryption time per layer (avg): 42ms
- Decryption time per layer (avg): 38ms
- Multiplicative depth required: 2 (sufficient for weighted averaging)
- Estimated total per-round overhead: ~1.8s for 3-hospital scenario

### Blockers
- Need TenSEAL context params from Kushi to run end-to-end test
- PyTorch gradient hooks need testing with encrypted weight serialization

### Tomorrow
- Implement gradient compatibility shim
- Run profiling on full model weight vector encryption
