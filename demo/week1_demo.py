"""
Member 5 - Integration & QA
Task: Week 1 End-to-End Demo Script
Day 4-5: Run FL server + 3 hospital nodes, complete 3 FL rounds, print metrics
"""

import os
import sys
import time
import threading
import subprocess

from utils.logger import get_logger

logger = get_logger("Week1Demo")

BANNER = """
╔══════════════════════════════════════════════════════╗
║       FedMed — Week 1 Demo                          ║
║       Cross-Silo Federated Learning Engine           ║
║       3 Hospital Nodes | 3 FL Rounds | BraTS 2021   ║
╚══════════════════════════════════════════════════════╝
"""

DATA_DIR = "data/raw/brats2021"
SERVER_ADDR = "localhost:8080"
NUM_ROUNDS = 3


def check_data_available() -> bool:
    """Check if BraTS data exists before starting demo."""
    if not os.path.exists(DATA_DIR):
        logger.warning(f"BraTS data not found at '{DATA_DIR}'")
        logger.warning("Running demo with DUMMY DATA (random tensors)")
        logger.warning("Download BraTS 2021 from https://www.synapse.org for real training")
        return False
    return True


def run_server():
    """Start FL server in background thread."""
    from server.fl_server import start_server
    logger.info("Starting FL Server on port 8080...")
    start_server(server_address=SERVER_ADDR, num_rounds=NUM_ROUNDS)


def run_hospital_node(hospital_id: int):
    """Start a hospital node client in background thread."""
    time.sleep(3)  # Wait for server to be ready
    from client.fl_client import start_hospital_node
    logger.info(f"Starting Hospital Node {hospital_id}...")
    start_hospital_node(
        hospital_id=hospital_id,
        server_address=SERVER_ADDR,
        data_dir=DATA_DIR,
    )


def main():
    print(BANNER)

    # Pre-flight checks
    data_available = check_data_available()
    logger.info(f"Data available: {data_available}")
    logger.info(f"FL Rounds: {NUM_ROUNDS}")
    logger.info(f"Hospital Nodes: 3")
    logger.info("-" * 50)

    # Launch FL server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Give server time to start

    # Launch 3 hospital nodes in parallel threads
    hospital_threads = []
    for hospital_id in [1, 2, 3]:
        t = threading.Thread(
            target=run_hospital_node,
            args=(hospital_id,),
            daemon=True,
        )
        hospital_threads.append(t)
        t.start()
        time.sleep(0.5)  # Stagger node startup

    # Wait for all nodes to complete
    logger.info("All nodes launched. Waiting for FL rounds to complete...")
    for t in hospital_threads:
        t.join(timeout=600)  # 10 minute timeout

    server_thread.join(timeout=60)

    logger.info("=" * 50)
    logger.info("  Week 1 Demo Complete!")
    logger.info("  Check logs/fedmed_*.log for detailed metrics")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
