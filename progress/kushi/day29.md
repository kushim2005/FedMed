# Day 29 — Sept 24 | Kushi | FL Systems

## Focus: TenSEAL Context Design + Server HE Architecture

### Tasks Completed
- Designed CKKS context parameters for FedMed:
  - poly_mod_degree: 8192
  - coeff_mod_bit_sizes: [60, 40, 40, 60]
  - global_scale: 2^40
  - Security level: 128-bit
- Implemented `encryption/tenseal_context.py`:
  - `create_ckks_context()` — create and return context
  - `save_context(ctx, path)` — serialize to disk
  - `load_context(path)` — load from disk
  - `get_public_key_bytes(ctx)` — extract public key for client distribution
- Designed server HE aggregation architecture:
  - Server holds public key only
  - Clients encrypt weights with public key
  - Server aggregates over ciphertexts (no decryption)
  - Global model holder decrypts with secret key

### Tomorrow
- Implement `server/fl_server_v3.py` with HE aggregation support
