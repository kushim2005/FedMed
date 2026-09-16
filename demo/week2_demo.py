"""
demo/week2_demo.py
Member 4 - Vasu Sree (Backend / DevOps) & Member 1 - Ravi (Integration)
Week 2: End-to-End Demonstration Script for FedMed.

Demonstrates:
1. Automated TLS certificate generation (Root CA + Server + 3 Clients)
2. Dirichlet non-IID data partitioning
3. Multi-node Federated Learning training loop (Server + 3 Hospitals)
4. Model evaluation & checkpoint generation
"""

import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(ROOT_DIR))

from security.generate_certs import generate_all_certs
from security.tls_config import certs_exist
from train.federated_train import run_federated_training


def main():
    print("=" * 70)
    print("🏥  FedMed: Week 2 Cross-Silo Federated Learning Demo  🧠")
    print("=" * 70)
    print("Domain: Privacy-Preserving Machine Learning in Healthcare")
    print("Task:   3D Brain Tumor Segmentation (BraTS 2021)")
    print("Nodes:  1 FL Server + 3 Global Hospital Nodes (AIIMS, Mayo, NHS)")
    print("Privacy: TLS-Encrypted gRPC Communication Channels")
    print("=" * 70)

    # 1. Generate certs if needed
    if not certs_exist():
        print("\n[Demo Step 1] Initializing PKI & generating TLS Certificates...")
        generate_all_certs(num_hospitals=3)
    else:
        print("\n[Demo Step 1] Verified TLS certificates in security/certs/")

    # 2. Run simulation
    print("\n[Demo Step 2] Launching 3-Round Federated Training Demo...")
    run_federated_training(
        rounds=3,
        data_dir="dataset/BraTS2021",
        num_hospitals=3,
        alpha=0.8,
        use_tls=True,
    )

    print("\n" + "=" * 70)
    print("🎉  FedMed Week 2 Demo Complete!")
    print("Checkpoints: checkpoints/global_model_round_*.pt")
    print("Metrics:     results/server_round_metrics.json")
    print("=" * 70)


if __name__ == "__main__":
    main()
