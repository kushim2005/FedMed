"""
train/federated_train.py
Member 1 - Chaitanya (ML Lead)
Week 2: End-to-End Federated Training Runner & Process Orchestrator.

Orchestrates:
1. Cert verification / generation
2. Dataset partitioning across 3 hospital nodes
3. Server launching (sub-process with TLS)
4. Client spawning (3 hospital nodes in parallel)
5. Metric aggregation and summary reporting
"""

import sys
import time
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(ROOT_DIR))

from security.generate_certs import generate_all_certs
from security.tls_config import certs_exist
from data.partition import partition_brats_dataset


def run_federated_training(
    rounds: int = 5,
    data_dir: str = "dataset/BraTS2021",
    num_hospitals: int = 3,
    alpha: float = 0.5,
    use_tls: bool = True,
):
    print("=" * 65)
    print("🧠 FedMed: Privacy-Preserving Cross-Silo FL (Week 2)")
    print("=" * 65)

    # 1. Certificates
    if use_tls and not certs_exist():
        print("\n[Step 1/4] Generating TLS Certificates...")
        generate_all_certs(num_hospitals=num_hospitals)
    else:
        print("\n[Step 1/4] TLS Certificates ready.")

    # 2. Partition Data
    print(f"\n[Step 2/4] Partitioning BraTS dataset (Dirichlet alpha={alpha})...")
    partition_file = ROOT_DIR / "data" / "partition_map.json"
    partition_brats_dataset(
        data_dir=data_dir,
        output_json=str(partition_file),
        num_clients=num_hospitals,
        alpha=alpha,
    )
    print(f"Partition map saved to: {partition_file}")

    # 3. Start Server Process
    print(f"\n[Step 3/4] Launching FL Server ({rounds} rounds)...")
    server_cmd = [
        sys.executable,
        str(ROOT_DIR / "server" / "fl_server_v2.py"),
        "--rounds",
        str(rounds),
        "--port",
        "8080",
    ]
    if not use_tls:
        server_cmd.append("--no-tls")

    server_process = subprocess.Popen(server_cmd, cwd=str(ROOT_DIR))
    time.sleep(3)  # Allow server to bind port

    # 4. Start Hospital Clients
    print(f"\n[Step 4/4] Starting {num_hospitals} Hospital Client Nodes...")
    client_processes = []
    for hid in range(1, num_hospitals + 1):
        client_cmd = [
            sys.executable,
            str(ROOT_DIR / "client" / "fl_client_v2.py"),
            "--hospital-id",
            str(hid),
            "--server",
            "127.0.0.1:8080",
            "--data-dir",
            data_dir,
        ]
        if not use_tls:
            client_cmd.append("--no-tls")

        proc = subprocess.Popen(client_cmd, cwd=str(ROOT_DIR))
        client_processes.append(proc)
        time.sleep(1)

    print("\nTraining in progress across distributed hospital silos...")
    server_process.wait()
    for cp in client_processes:
        cp.wait()

    print("\n✅ Federated Training Completed Successfully!")
    print("Checkpoints saved in: checkpoints/")
    print("Metrics report saved in: results/")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="FedMed Federated Training")
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--data-dir", type=str, default="dataset/BraTS2021")
    parser.add_argument("--no-tls", action="store_true")
    parser.add_argument("--alpha", type=float, default=0.5)
    args = parser.parse_args()

    run_federated_training(
        rounds=args.rounds,
        data_dir=args.data_dir,
        alpha=args.alpha,
        use_tls=not args.no_tls,
    )
