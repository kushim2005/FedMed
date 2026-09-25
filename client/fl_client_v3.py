"""
client/fl_client_v3.py
FedMed — Federated Learning Client with Homomorphic Encryption.

Author: Ravi (Integration Lead)
Week 3: HE-enabled Hospital Client

Extends fl_client_v2 (TLS + backoff retry) with CKKS encryption:
  - Encrypts local model weights before transmitting to server
  - Server only receives ciphertexts — never sees plaintext weights
  - Decrypts aggregated global model received from server
  - Hospital's secret key never leaves the local environment

Weight transport protocol:
  state_dict → sorted numpy arrays → CKKS ciphertexts → base64 → NDArray
"""

import os
import logging
from collections import OrderedDict
from typing import Dict, List, Tuple

import numpy as np
import torch
import flwr as fl
from flwr.common import (
    FitIns,
    FitRes,
    Parameters,
    Scalar,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
)

from model.unet3d import build_model
from data.dataset import get_dataloaders
from utils.logger import get_logger
from encryption.tenseal_context import context_from_bytes, load_context
from encryption.he_aggregator import (
    encrypt_weights,
    decrypt_weights,
    ciphertexts_to_ndarray,
    ndarray_to_ciphertexts,
)

logger = get_logger("fl_client_v3")

HE_ENABLED = os.environ.get("HE_ENABLED", "true").lower() == "true"
HOSPITAL_ID = os.environ.get("HOSPITAL_ID", "hospital_0")
DATA_DIR = os.environ.get("DATA_DIR", "data/raw")
DEVICE = os.environ.get("DEVICE", "cpu")
CONTEXT_PATH = os.environ.get("HE_CONTEXT_PATH", "keys/ckks_context.tenseal")
LOCAL_EPOCHS = int(os.environ.get("LOCAL_EPOCHS", "2"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "2"))
LEARNING_RATE = float(os.environ.get("LEARNING_RATE", "1e-4"))


class HEFedMedClient(fl.client.NumPyClient):
    """
    Hospital FL client with homomorphic encryption weight protection.

    Before transmitting weights to the server, each layer's values are
    encrypted using the CKKS scheme. The server aggregates over
    ciphertexts and broadcasts the decrypted global model back.
    """

    def __init__(
        self,
        hospital_id: str,
        data_dir: str,
        device: str = "cpu",
        context_path: str = CONTEXT_PATH,
        he_enabled: bool = HE_ENABLED,
    ):
        """
        Initialize the HE-enabled hospital client.

        Args:
            hospital_id: Unique hospital identifier (e.g., 'aiims_delhi').
            data_dir: Path to the local BraTS data directory.
            device: PyTorch device string ('cpu' or 'cuda').
            context_path: Path to the CKKS context file (must contain secret key
                for decryption; public key for encryption).
            he_enabled: Enable homomorphic encryption. Falls back to
                plaintext FedAvg if False or if context is unavailable.
        """
        self.hospital_id = hospital_id
        self.device = torch.device(device)
        self.he_enabled = he_enabled
        self.context = None
        self.weight_shapes: List[tuple] = []

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

        if self.he_enabled:
            self._load_context(context_path)

        logger.info(
            "HEFedMedClient initialized: hospital=%s, he=%s, device=%s",
            hospital_id,
            he_enabled,
            device,
        )

    def _load_context(self, path: str) -> None:
        """Load CKKS context from disk."""
        try:
            self.context = load_context(path)
            logger.info("CKKS context loaded from %s", path)
        except FileNotFoundError:
            logger.warning(
                "CKKS context not found at %s — HE disabled for this client",
                path,
            )
            self.he_enabled = False

    def _get_weight_arrays(self) -> Tuple[List[np.ndarray], List[str], List[tuple]]:
        """
        Extract model weights as sorted numpy arrays.

        Returns:
            Tuple of (arrays, keys, shapes) in canonical sorted key order.
        """
        state_dict = self.model.state_dict()
        sorted_keys = sorted(state_dict.keys())
        arrays = []
        shapes = []

        for key in sorted_keys:
            arr = state_dict[key].cpu().numpy()
            arrays.append(arr)
            shapes.append(arr.shape)

        return arrays, sorted_keys, shapes

    def _set_weight_arrays(
        self, arrays: List[np.ndarray], keys: List[str]
    ) -> None:
        """Load weight arrays back into the model state dict."""
        state_dict = OrderedDict()
        for key, arr in zip(keys, arrays):
            state_dict[key] = torch.tensor(arr, device=self.device)
        self.model.load_state_dict(state_dict, strict=True)

    def get_parameters(self, config: Dict) -> List[np.ndarray]:
        """
        Return encrypted model weights for transmission to the server.

        If HE is enabled, encrypts each layer's weight array as a CKKS
        ciphertext and packs them as numpy byte arrays. Appends shape
        metadata as the final element so the server can reconstruct shapes.

        Args:
            config: Flower configuration dict (unused).

        Returns:
            List of numpy arrays. If HE enabled: [ct_arr_0, ..., ct_arr_N, shapes_arr].
            If HE disabled: standard plaintext numpy arrays.
        """
        arrays, keys, shapes = self._get_weight_arrays()
        self._current_keys = keys

        if not self.he_enabled or self.context is None:
            return arrays

        ciphertexts = encrypt_weights(arrays, self.context)
        ct_ndarrays = [ciphertexts_to_ndarray([ct]) for ct in ciphertexts]

        shapes_arr = np.array(
            [list(s) + [0] * (4 - len(s)) for s in shapes], dtype=np.int32
        )
        ct_ndarrays.append(shapes_arr)

        logger.debug(
            "Encrypted %d weight tensors for hospital %s",
            len(ciphertexts),
            self.hospital_id,
        )
        return ct_ndarrays

    def set_parameters(self, parameters: List[np.ndarray]) -> None:
        """
        Update local model with decrypted aggregated global weights.

        Args:
            parameters: Aggregated parameters from server. Plaintext
                numpy arrays (server decrypts before broadcasting).
        """
        arrays, _, keys = self._get_weight_arrays()

        if len(parameters) != len(arrays):
            logger.warning(
                "Parameter count mismatch: got %d, expected %d",
                len(parameters),
                len(arrays),
            )

        clipped = [
            p[: int(np.prod(s))].reshape(s)
            for p, s in zip(parameters, [a.shape for a in arrays])
        ]
        self._set_weight_arrays(clipped, sorted(self.model.state_dict().keys()))

    def fit(
        self, parameters: List[np.ndarray], config: Dict
    ) -> Tuple[List[np.ndarray], int, Dict[str, Scalar]]:
        """
        Train for LOCAL_EPOCHS and return encrypted weights.

        Args:
            parameters: Initial global model parameters from server.
            config: Training config dict (may contain 'proximal_mu').

        Returns:
            Tuple of (encrypted_params, num_examples, metrics).
        """
        self.set_parameters(parameters)

        mu = float(config.get("proximal_mu", 0.01))
        global_weights = [
            p.clone() for p in self.model.parameters()
        ]

        self.model.train()
        total_loss = 0.0
        num_examples = 0

        from monai.losses import DiceCELoss
        criterion = DiceCELoss(to_onehot_y=True, softmax=True)

        for epoch in range(LOCAL_EPOCHS):
            for batch in self.train_loader:
                images = batch["image"].to(self.device)
                labels = batch["label"].to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = criterion(outputs, labels)

                prox_term = 0.0
                for p, g in zip(self.model.parameters(), global_weights):
                    prox_term += (mu / 2) * torch.norm(p - g) ** 2
                loss = loss + prox_term

                loss.backward()
                self.optimizer.step()

                total_loss += loss.item() * images.size(0)
                num_examples += images.size(0)

        avg_loss = total_loss / max(num_examples, 1)
        logger.info(
            "Hospital %s: %d epochs, %d samples, loss=%.4f",
            self.hospital_id,
            LOCAL_EPOCHS,
            num_examples,
            avg_loss,
        )

        encrypted_params = self.get_parameters(config={})
        return encrypted_params, num_examples, {"loss": avg_loss}

    def evaluate(
        self, parameters: List[np.ndarray], config: Dict
    ) -> Tuple[float, int, Dict[str, Scalar]]:
        """
        Evaluate the global model on local validation data.

        Args:
            parameters: Global model parameters to evaluate.
            config: Evaluation config dict.

        Returns:
            Tuple of (loss, num_examples, metrics).
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

        logger.info(
            "Hospital %s eval: loss=%.4f, dice=%.4f",
            self.hospital_id,
            avg_loss,
            dice,
        )
        return avg_loss, num_examples, {"dice": dice}


def start_he_client(
    server_address: str = "localhost:8080",
    hospital_id: str = HOSPITAL_ID,
    data_dir: str = DATA_DIR,
) -> None:
    """
    Connect and run the HE-enabled FL client.

    Args:
        server_address: FL server address (host:port).
        hospital_id: Unique identifier for this hospital node.
        data_dir: Path to local BraTS data.
    """
    client = HEFedMedClient(
        hospital_id=hospital_id,
        data_dir=data_dir,
        device=DEVICE,
        context_path=CONTEXT_PATH,
        he_enabled=HE_ENABLED,
    )

    logger.info(
        "Starting HE client: hospital=%s → server=%s (HE=%s)",
        hospital_id,
        server_address,
        HE_ENABLED,
    )

    fl.client.start_numpy_client(
        server_address=server_address,
        client=client,
    )
