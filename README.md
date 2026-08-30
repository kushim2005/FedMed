# FedMed: Cross-Silo Federated Learning Engine

A privacy-preserving federated learning platform for collaborative brain tumor segmentation across hospitals — without sharing raw patient data.

## Domain
Privacy-Preserving Machine Learning (PPML) & Healthcare

## Problem Statement
Training highly accurate ML models for rare diseases requires massive patient datasets. Strict data privacy laws (HIPAA/GDPR) prevent hospitals from sharing raw patient data. FedMed solves this by training locally and sharing only encrypted weight updates.

## Architecture
- **Federated Learning**: Flower (flwr) framework
- **Model**: 3D U-Net via PyTorch + MONAI
- **Encryption**: TenSEAL (Homomorphic Encryption - CKKS)
- **Dashboard**: React + Recharts
- **Communication**: gRPC over mTLS

## Week 1 Team
| Member | Role | Branch |
|--------|------|--------|
| Member 1 | ML Lead — 3D U-Net Architecture | feature/member1/unet-architecture |
| Member 2 | ML Engineer — Data Pipeline & Eval | feature/member2/data-preprocessing |
| Member 3 | FL Systems Lead — Flower Server | feature/member3/fl-server |
| Member 4 | Backend/DevOps — Hospital Nodes | feature/member4/hospital-nodes |
| Member 5 | Integration & QA | feature/member5/integration |

## ⚠️ Dataset Setup (Do NOT commit data to GitHub)

BraTS 2021 dataset is NOT included in this repository.
Each member must download it independently:

1. Register at https://www.synapse.org
2. Request access to BraTS 2021 (syn27046444)
3. Accept data use agreement
4. Download and place in `data/raw/brats2021/`

The `data/raw/` folder is gitignored — MRI data will never be pushed.

## Setup

```bash
# Clone the repo
git clone https://github.com/<your-org>/fedmed.git
cd fedmed

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Running Week 1 Demo

```bash
# Start FL server
python server/fl_server.py

# Start hospital nodes (in separate terminals)
python client/fl_client.py --hospital-id 1 --port 8081
python client/fl_client.py --hospital-id 2 --port 8082
python client/fl_client.py --hospital-id 3 --port 8083

# Or run full demo
python demo/week1_demo.py
```

## Project Structure

```
fedmed/
├── model/          # 3D U-Net architecture (Member 1)
├── train/          # Training scripts (Member 1)
├── data/           # Preprocessing & dataset (Member 2)
├── eval/           # Metrics & evaluation (Member 2)
├── server/         # Flower FL server (Member 3)
├── client/         # Hospital node clients (Member 4)
├── demo/           # End-to-end demo (Member 5)
├── utils/          # Logging & utilities (Member 5)
├── tests/          # Unit tests
└── logs/           # Training logs (gitignored)
```
