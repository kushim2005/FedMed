"""
client/fl_client_dp.py
FedMed — Federated Learning Client with Differential Privacy (DP-SGD).

Author: Kushi (FL Systems)
Week 4: Privacy-Preserving Hospital Client

Extends fl_client_v3 with Opacus DP-SGD:
  - Per-sample gradient clipping (C = max_grad_norm)
  - Calibrated Gaussian noise (σ = noise_multiplier * C)
  - Rényi DP accounting: tracks epsilon per round
  - Budget enforcement: stops training if ε > max_epsilon
  - Reports epsilon to server in FitRes metrics
"""

import os
import logging
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import flwr as fl
from flwr.common import Scalar

from model.unet3d import build_model
from data.dataset import get_dataloaders
from utils.logger import get_logger
from privacy.dp_trainer import DPTrainer
from privacy.privacy_budget import PrivacyBudget

logger = get_logger("fl_client_dp")

HOSPITAL_ID = os.environ.get("HOSPITAL_ID", "hospital_0")
DATA_DIR = os.environ.get("DATA_DIR", "data/raw")
DEVICE = os.environ.get("DEVICE", "cpu")
DP_ENABLED = os.environ.get("DP_ENABLED", "true").lower() == "true"
NOISE_MULTIPLIER = float(os.environ.get("NOISE_MULTIPLIER", "1.1"))
MAX_GRAD_NORM = float(os.environ.get("MAX_GRAD_NORM", "1.0"))
TARGET_DELTA = float(os.environ.get("TARGET_DELTA", "1e-5"))
MAX_EPSILON = float(os.environ.get("MAX_EPSILON", "3.5"))
LOCAL_EPOCHS = int(os.environ.get("LOCAL_EPOCHS", "2"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "2"))
LEARNING_RATE = float(os.environ.get("LEARNING_RATE", "1e-4"))
SERVER_ADDRESS = os.environ.get("FL_SERVER_ADDRESS", "localhost:8080")


class DPFedMedClient(fl.client.NumPyClient):
    """
    Hospital FL client with Differential Privacy via DP-SGD.

    Wraps local training with Opacus PrivacyEngine, ensuring that each
    hospital's training data is protected by (ε, δ)-DP before gradients
    influence the federated global model.
    """

    def __init__(
        self,
        hospital_id: str,
        data_dir: str,
        device: str = "cpu",
        dp_enabled: bool = DP_ENABLED,
        noise_multiplier: float = NOISE_MULTIPLIER,
        max_grad_norm: float = MAX_GRAD_NORM,
        delta: float = TARGET_DELTA,
        max_epsilon: float = MAX_EPSILON,
    ):
        """
        Initialize the DP-enabled hospital client.

        Args:
            hospital_id: Unique hospital identifier.
            data_dir: Local BraTS data directory.
            device: PyTorch device ('cpu' or 'cuda').
            dp_enabled: Activate DP-SGD (fallback to standard SGD if False).
            noise_multiplier: Gaussian noise multiplier σ. Default 1.1
                gives ε≈2.8 for 10 rounds (Chaitanya's analysis).
            max_grad_norm: Gradient clipping bound C. Default 1.0.
            delta: Privacy failure probability δ. Default 1e-5.
            max_epsilon: Maximum allowed cumulative ε. Default 3.5.
        """
        self.hospital_id = hospital_id
        self.device = torch.device(device)
        self.dp_enabled = dp_enabled
        self.noise_multiplier = noise_multiplier
        self.max_grad_norm = max_grad_norm
        self.delta = delta
        self.max_epsilon = max_epsilon
        self.round_id = 0

        self.model = build_model(self.device)
        self.train_loader, self.val_loader = get_dataloaders(
            data_dir=data_dir,
            batch_size=BATCH_SIZE,
            num_workers=0,
            hospital_id=hospital_id,
        )
        self.optimizer = torch.optim.Adam(
            self.model.parameters(), lr=LEARNING_RATE
        )

        self.budget = PrivacyBudget(
            max_epsilon=max_epsilon,
            delta=delta,
            noise_multiplier=noise_multiplier,
            max_grad_norm=max_grad_norm,
        )

        self.dp_trainer = DPTrainer(
            model=self.model,
            optimizer=self.optimizer,
            data_loader=self.train_loader,
            noise_multiplier=noise_multiplier,
            max_grad_norm=max_grad_norm,
            delta=delta,
            max_epsilon=max_epsilon,
            enabled=dp_enabled,
        )

        self.model = self.dp_trainer.model
        self.optimizer = self.dp_trainer.optimizer
        self.train_loader = self.dp_trainer.data_loader

        logger.info(
            "DPFedMedClient: hospital=%s, DP=%s, σ=%.2f, C=%.1f, max_ε=%.1f",
            hospital_id,
            dp_enabled,
            noise_multiplier,
            max_grad_norm,
            max_epsilon,
        )

    def get_parameters(self, config: Dict) -> List[np.ndarray]:
        """Return current model parameters as numpy arrays."""
        state_dict = self.model.state_dict()
        return [
            v.cpu().numpy() for _, v in sorted(state_dict.items())
        ]

    def set_parameters(self, parameters: List[np.ndarray]) -> None:
        """Load server-aggregated parameters into the local model."""
        keys = sorted(self.model.state_dict().keys())
        state_dict = OrderedDict(
            {k: torch.tensor(v, device=self.device) for k, v in zip(keys, parameters)}
        )
        self.model.load_state_dict(state_dict, strict=True)

    def fit(
        self, parameters: List[np.ndarray], config: Dict
    ) -> Tuple[List[np.ndarray], int, Dict[str, Scalar]]:
        """
        Train locally with DP-SGD and return updated parameters.

        Checks budget before training — stops if epsilon exceeds max_epsilon.

        Args:
            parameters: Global model parameters from server.
            config: Training config (may contain 'proximal_mu').

        Returns:
            Tuple (parameters, num_examples, metrics) where metrics
            includes 'epsilon' and 'delta' for server-side tracking.
        """
        self.set_parameters(parameters)
        self.round_id += 1

        epsilon, delta = self.dp_trainer.get_privacy_spent()

        if self.dp_trainer.is_budget_exceeded():
            logger.warning(
                "Hospital %s: budget exceeded (ε=%.4f > %.1f), "
                "skipping local training",
                self.hospital_id,
                epsilon,
                self.max_epsilon,
            )
            return self.get_parameters(config={}), 0, {
                "epsilon": epsilon,
                "delta": delta,
                "budget_exceeded": 1.0,
            }

        from monai.losses import DiceCELoss
        criterion = DiceCELoss(to_onehot_y=True, softmax=True)

        global_params = [p.clone().detach() for p in self.model.parameters()]
        mu = float(config.get("proximal_mu", 0.01))

        total_loss = 0.0
        num_examples = 0

        for _ in range(LOCAL_EPOCHS):
            epoch_loss, epoch_epsilon = self.dp_trainer.train_one_epoch(
                criterion=criterion,
                device=self.device,
                proximal_mu=mu,
                global_params=global_params,
            )
            total_loss += epoch_loss

            if self.dp_trainer.is_budget_exceeded():
                logger.warning(
                    "Hospital %s: budget exhausted mid-training (ε=%.4f)",
                    self.hospital_id,
                    epoch_epsilon,
                )
                break

            num_examples += BATCH_SIZE * len(self.train_loader)

        avg_loss = total_loss / LOCAL_EPOCHS
        epsilon, delta = self.dp_trainer.get_privacy_spent()

        self.budget.step(
            sample_rate=BATCH_SIZE / max(len(self.train_loader.dataset), 1),
            steps=LOCAL_EPOCHS * len(self.train_loader),
        )

        self.dp_trainer.log_privacy_status(self.round_id)

        logger.info(
            "Hospital %s Round %d: loss=%.4f, ε=%.4f, samples=%d",
            self.hospital_id,
            self.round_id,
            avg_loss,
            epsilon,
            num_examples,
        )

        return self.get_parameters(config={}), num_examples, {
            "loss": avg_loss,
            "epsilon": epsilon,
            "delta": delta,
            "round": float(self.round_id),
        }

    def evaluate(
        self, parameters: List[np.ndarray], config: Dict
    ) -> Tuple[float, int, Dict[str, Scalar]]:
        """
        Evaluate global model on local validation data.

        Args:
            parameters: Global model parameters.
            config: Evaluation config dict.

        Returns:
            Tuple (loss, num_examples, metrics).
        """
        self.set_parameters(parameters)
        self.model.eval()

        from monai.losses import DiceLoss
        from monai.metrics import DiceMetric

        criterion = DiceLoss(to_onehot_y=True, softmax=True)
        dice_metric = DiceMetric(include_background=False, reduction="mean")

        total_loss = 0.0
        num_examples = 0

        with torch.no_grad():
            for batch in self.val_loader:
                images = batch["image"].to(self.device)
                labels = batch["label"].to(self.device)

                outputs = self.model(images)
                loss = criterion(outputs, labels)

                preds = torch.argmax(outputs, dim=1, keepdim=True)
                dice_metric(y_pred=preds, y=labels)

                total_loss += loss.item() * images.size(0)
                num_examples += images.size(0)

        avg_loss = total_loss / max(num_examples, 1)
        dice = dice_metric.aggregate().item()
        dice_metric.reset()

        epsilon, _ = self.dp_trainer.get_privacy_spent()

        logger.info(
            "Hospital %s eval: loss=%.4f, dice=%.4f, ε=%.4f",
            self.hospital_id,
            avg_loss,
            dice,
            epsilon,
        )
        return avg_loss, num_examples, {"dice": dice, "epsilon": epsilon}


def start_dp_client(
    server_address: str = SERVER_ADDRESS,
    hospital_id: str = HOSPITAL_ID,
    data_dir: str = DATA_DIR,
) -> None:
    """
    Start the DP-enabled FL client.

    Args:
        server_address: FL server address (host:port).
        hospital_id: Unique hospital identifier.
        data_dir: Path to local BraTS dataset.
    """
    client = DPFedMedClient(
        hospital_id=hospital_id,
        data_dir=data_dir,
        device=DEVICE,
        dp_enabled=DP_ENABLED,
        noise_multiplier=NOISE_MULTIPLIER,
        max_grad_norm=MAX_GRAD_NORM,
        delta=TARGET_DELTA,
        max_epsilon=MAX_EPSILON,
    )

    logger.info(
        "Starting DP client: hospital=%s → %s (DP=%s, σ=%.2f)",
        hospital_id,
        server_address,
        DP_ENABLED,
        NOISE_MULTIPLIER,
    )

    fl.client.start_numpy_client(
        server_address=server_address,
        client=client,
    )
