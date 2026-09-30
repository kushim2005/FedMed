# FedMed Changelog

All notable changes to the FedMed project are documented in this file.
Follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

## [1.0.0] - 2026-09-30

### Added (Week 4 — Sept 28-30)
- **DP-SGD**: Opacus PrivacyEngine with per-sample gradient clipping and Gaussian noise
- **Privacy Budget**: Rényi DP accounting with configurable epsilon cap (max_epsilon=3.5)
- **fl_client_dp.py**: DP-enabled hospital client with per-round epsilon reporting
- **React Dashboard**: Full SPA with dark theme, Recharts convergence chart, privacy bar
- **FastAPI backend**: Metrics server serving live training data to dashboard
- **nginx proxy**: Reverse proxy routing `/` to dashboard, `/api` to FastAPI

### Result: Dice=0.683, ε=2.79 at δ=1e-5 ✅

---

## [0.3.0] - 2026-09-27

### Added (Week 3 — Sept 23-27)
- **TenSEAL CKKS**: 128-bit homomorphic encryption (poly_n=8192, scale=2^40)
- **fl_server_v3.py**: HE-enabled server — aggregates over ciphertexts
- **fl_client_v3.py**: HE-enabled client — encrypts weights before transmission
- **he_aggregator.py**: Weighted FedAvg over CKKS ciphertexts
- **test_he_encryption.py**: 5 unit tests (context, roundtrip, aggregation, keys, edge cases)

### Result: Dice=0.691, 128-bit IND-CPA security ✅

---

## [0.2.0] - 2026-09-22

### Added (Week 2 — Sept 3-22)
- **TLS gRPC**: RSA-2048 CA + server/client certificates (mutual TLS)
- **FedProx**: Proximal term (μ=0.01) for heterogeneous client regularization
- **Non-IID Partitioning**: Dirichlet (α=0.8) data distribution across hospitals
- **Checkpointing**: Best model saved per round, resume on failure
- **fl_server_v2.py / fl_client_v2.py**: Production-ready TLS FL stack

### Result: Dice=0.712, TLS secured ✅

---

## [0.1.0] - 2026-09-02

### Added (Week 1 — Aug 26 - Sep 2)
- **3D U-Net**: MONAI-based FedMed3DUNet for brain tumor segmentation
- **BraTS 2021 Pipeline**: Data loading, preprocessing (intensity norm, random crops)
- **Flower Integration**: Basic FL with FedAvg strategy
- **Basic FL**: Centralised baseline Dice=0.72

### Result: Federated Dice=0.706, Centralized=0.72 ✅
