# FedMed Demo Scripts

This directory contains standalone, end-to-end execution scripts for each phase of the FedMed project.

## Scripts Overview

| Script | Phase | Description | Key Modules Tested |
|---|---|---|---|
| `week3_demo.py` | Week 3 | Homomorphic Encryption (CKKS) | `encryption/tenseal_context.py`, `encryption/he_aggregator.py`, `server/fl_server_v3.py`, `client/fl_client_v3.py` |
| `week4_demo.py` | Week 4 | Differential Privacy (DP-SGD) | `privacy/dp_trainer.py`, `privacy/privacy_budget.py`, `client/fl_client_dp.py`, `api/metrics_server.py` |

## Usage Examples

### Running Week 3 Demo (Homomorphic Encryption)
Simulates FL with CKKS encryption over 10 rounds across 3 simulated hospital nodes (AIIMS Delhi, Mayo Clinic, NHS London):
```bash
python demo/week3_demo.py --rounds 10 --he-enabled
```

To run with plaintext fallback:
```bash
python demo/week3_demo.py --rounds 10 --no-he
```

### Running Week 4 Demo (Differential Privacy)
Runs DP-SGD training with per-sample clipping and calibrated Gaussian noise:
```bash
python demo/week4_demo.py --rounds 10 --sigma 1.1 --clip 1.0 --max-epsilon 3.5
```
Live metrics can be observed in the web dashboard at `http://localhost:3000`.
