"""
Member 4 - Backend/DevOps
Task: Hospital Node FL Clients
Day 1-5: Implement 3 mock hospital nodes using Flower NumPyClient
"""

import sys
import os
import argparse
from collections import OrderedDict
from typing import Dict, List, Tuple

import flwr as fl
import torch
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.unet3d import build_model
from data.dataset import get_dataloaders
from eval.metrics import compute_dice_score
from utils.logger import get_logger


HOSPITAL_NAMES = {
    1: "Hospital-A (AIIMS)",
    2: "Hospital-B (Mayo Clinic)",
    3: "Hospital-C (NHS Trust)",
}


class HospitalClient(fl.client.NumPyClient):
    """
    FedMed Hospital Node — Flower NumPyClient.

    Each hospital node:
      1. Receives global model weights from FL server
      2. Trains on local private MRI data for E epochs
      3. Returns updated weights + training metrics
      4. Raw patient data NEVER leaves this node
    """

    def __init__(
        self,
        hospital_id: int,
        data_dir: str,
        device: str = "cpu",
    ):
        self.hospital_id = hospital_id
        self.hospital_name = HOSPITAL_NAMES.get(hospital_id, f"Hospital-{hospital_id}")
        self.device = torch.device(device)
        self.logger = get_logger(f"Node-{self.hospital_name}")

        # Initialize local model
        self.model = build_model(device)

        # Load this hospital's data partition
        self.train_loader, self.val_loader = get_dataloaders(
            data_dir=data_dir,
            batch_size=1,
            num_workers=2,
            hospital_id=hospital_id,
        )

        self.logger.info(f"{self.hospital_name} node initialized")
        self.logger.info(f"Train batches: {len(self.train_loader)}")

    def get_parameters(self, config: Dict) -> List[np.ndarray]:
        """Extract model parameters as numpy arrays for FL server."""
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def set_parameters(self, parameters: List[np.ndarray]):
        """Load global model parameters received from FL server."""
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = OrderedDict({
            k: torch.tensor(v) for k, v in params_dict
        })
        self.model.load_state_dict(state_dict, strict=True)

    def fit(
        self,
        parameters: List[np.ndarray],
        config: Dict,
    ) -> Tuple[List[np.ndarray], int, Dict]:
        """
        Local training step — called each FL round.

        1. Load global model weights from server
        2. Train on local private data for E epochs
        3. Return updated weights + num_examples + metrics
        """
        server_round = config.get("server_round", 0)
        local_epochs = config.get("local_epochs", 3)
        lr = config.get("learning_rate", 1e-4)
        proximal_mu = config.get("proximal_mu", 0.1)

        self.logger.info(
            f"Round {server_round} | {self.hospital_name} | "
            f"Local epochs: {local_epochs}"
        )

        # Load global weights
        self.set_parameters(parameters)

        # Save global weights for proximal term computation
        global_params = [p.clone().detach() for p in self.model.parameters()]

        # Local optimizer
        from monai.losses import DiceCELoss
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        criterion = DiceCELoss(to_onehot_y=True, softmax=True)

        self.model.train()
        total_loss = 0.0
        num_examples = 0

        for epoch in range(local_epochs):
            for batch in self.train_loader:
                images = batch["image"].to(self.device)
                labels = batch["label"].to(self.device)

                optimizer.zero_grad()
                outputs = self.model(images)

                # Standard loss
                loss = criterion(outputs, labels)

                # FedProx proximal term: (mu/2) * ||w - w_global||^2
                proximal_term = 0.0
                for local_p, global_p in zip(self.model.parameters(), global_params):
                    proximal_term += (local_p - global_p.to(self.device)).norm(2) ** 2
                loss += (proximal_mu / 2) * proximal_term

                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()

                total_loss += loss.item()
                num_examples += images.shape[0]

        avg_loss = total_loss / (local_epochs * len(self.train_loader))
        self.logger.info(f"Round {server_round} | Train Loss: {avg_loss:.4f}")

        return self.get_parameters(config={}), num_examples, {"train_loss": avg_loss}

    def evaluate(
        self,
        parameters: List[np.ndarray],
        config: Dict,
    ) -> Tuple[float, int, Dict]:
        """
        Local evaluation step — called each FL round after aggregation.

        Evaluates the global model on this hospital's local validation set.
        """
        self.set_parameters(parameters)
        self.model.eval()

        dice_scores = []
        num_examples = 0

        with torch.no_grad():
            for batch in self.val_loader:
                images = batch["image"].to(self.device)
                labels = batch["label"].to(self.device)
                outputs = self.model(images)
                dice = compute_dice_score(outputs, labels)
                dice_scores.append(dice)
                num_examples += images.shape[0]

        mean_dice = sum(dice_scores) / len(dice_scores) if dice_scores else 0.0
        loss = 1.0 - mean_dice  # Use (1 - Dice) as loss proxy

        self.logger.info(
            f"[Eval] {self.hospital_name} | "
            f"Dice: {mean_dice:.4f} | Samples: {num_examples}"
        )

        return loss, num_examples, {"dice_score": mean_dice}


def start_hospital_node(
    hospital_id: int,
    server_address: str = "localhost:8080",
    data_dir: str = "data/raw/brats2021",
):
    """Start a hospital FL client node and connect to FL server."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    client = HospitalClient(
        hospital_id=hospital_id,
        data_dir=data_dir,
        device=device,
    )

    logger = get_logger(f"Node-Launcher-{hospital_id}")
    logger.info(f"Connecting to FL server at {server_address}")

    fl.client.start_numpy_client(
        server_address=server_address,
        client=client,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FedMed Hospital Node")
    parser.add_argument("--hospital-id", type=int, required=True,
                        choices=[1, 2, 3], help="Hospital node ID (1, 2, or 3)")
    parser.add_argument("--server", type=str, default="localhost:8080",
                        help="FL server address")
    parser.add_argument("--data-dir", type=str, default="data/raw/brats2021",
                        help="Path to BraTS 2021 data")

    args = parser.parse_args()

    start_hospital_node(
        hospital_id=args.hospital_id,
        server_address=args.server,
        data_dir=args.data_dir,
    )
