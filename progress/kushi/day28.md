# Day 28 — Sept 23 | Kushi | FL Systems

## Focus: Week 2 Complete + HE Architecture Design (Week 3 Kickoff)

### Tasks Completed
- Confirmed Week 2 FL pipeline stable: TLS gRPC, FedProx (mu=0.01), checkpointing
- Week 3 HE architecture design session with team:
  - Selected CKKS scheme over BFV/BGV (supports approximate floats, ideal for weights)
  - Decided key distribution: server generates context, sends public key to clients
  - Aggregation protocol: server aggregates OVER ciphertexts (never decrypts raw weights)
  - Secret key stays at trusted coordinator only — never transmitted
- Designed CKKS context parameters for FedMed:
  - poly_mod_degree = 8192 (128-bit security)
  - coeff_mod_bit_sizes = [60, 40, 40, 60]
  - global_scale = 2^40
- Created `encryption/` folder structure skeleton
- Assigned team tasks:
  - Kushi: tenseal_context.py + fl_server_v3.py
  - Ravi: he_aggregator.py + fl_client_v3.py
  - Chaitanya: profiling + gradient compatibility
  - Ranjith: test suite
  - Vasu: Docker + containers

### Security Guarantee
- IND-CPA secure under RLWE assumption
- 128-bit classical security level
- Server learns nothing about individual client weights

### Tomorrow
- Implement encryption/tenseal_context.py
