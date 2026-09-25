"""
server/fl_server_v3.py
FedMed — Federated Learning Server with Homomorphic Encryption Aggregation.

Author: Kushi (FL Systems)
Week 3: HE-enabled FedProx Server

Extends fl_server_v2 (TLS + FedProx) with CKKS homomorphic encryption:
  - Receives encrypted client weights as Flower NDArrays
  - Aggregates over ciphertexts without decryption (server is untrusted)
  - Decrypts aggregated global weights using secret key
  - Broadcasts plaintext global model back to clients

Security guarantee: Server is computation-only; individual client
weights are never exposed in plaintext to the server.
"""

import os
import logging
import time
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import flwr as fl
from flwr.common import (
    FitIns,
    FitRes,
    Parameters,
    Scalar,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
)
from flwr.server.client_proxy import ClientProxy

from utils.logger import get_logger
from encryption.tenseal_context import create_ckks_context, save_context, load_context
from encryption.he_aggregator import (
    aggregate_encrypted_weights,
    ndarray_to_ciphertexts,
    decrypt_weights,
)

logger = get_logger("fl_server_v3")

HE_ENABLED = os.environ.get("HE_ENABLED", "true").lower() == "true"
CONTEXT_PATH = os.environ.get("HE_CONTEXT_PATH", "keys/ckks_context.tenseal")
ROUNDS = int(os.environ.get("FL_ROUNDS", "10"))
MIN_CLIENTS = int(os.environ.get("FL_MIN_CLIENTS", "2"))
SERVER_ADDRESS = os.environ.get("FL_SERVER_ADDRESS", "[::]:8080")


class HEFedAvgStrategy(fl.server.strategy.FedProx):
    """
    Federated Averaging strategy with Homomorphic Encryption aggregation.

    Extends FedProx to handle CKKS-encrypted weight updates from clients.
    When HE is enabled, aggregation is performed in the encrypted domain.
    Falls back to plaintext FedAvg if HE context is unavailable.
    """

    def __init__(
        self,
        context_path: str = CONTEXT_PATH,
        he_enabled: bool = HE_ENABLED,
        proximal_mu: float = 0.01,
        **kwargs,
    ):
        """
        Initialize the HE-enabled FedAvg strategy.

        Args:
            context_path: Path to the serialized CKKS context file.
            he_enabled: Whether to use homomorphic encryption aggregation.
            proximal_mu: FedProx proximal term coefficient.
        """
        super().__init__(proximal_mu=proximal_mu, **kwargs)
        self.he_enabled = he_enabled
        self.context_path = context_path
        self.context = None
        self.round_metrics: List[Dict] = []

        if self.he_enabled:
            self._load_or_create_context()

    def _load_or_create_context(self) -> None:
        """Load existing CKKS context or create a new one."""
        if os.path.exists(self.context_path):
            logger.info("Loading CKKS context from %s", self.context_path)
            self.context = load_context(self.context_path)
        else:
            logger.info("Creating new CKKS context (128-bit security)")
            self.context = create_ckks_context(
                poly_mod_degree=8192,
                coeff_mod_bit_sizes=[60, 40, 40, 60],
                global_scale=2 ** 40,
            )
            save_context(self.context, self.context_path, secret=True)
            logger.info("CKKS context saved to %s", self.context_path)

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        """
        Aggregate fit results using HE aggregation when enabled.

        Args:
            server_round: Current FL round number.
            results: List of (client, FitRes) tuples from participating clients.
            failures: List of clients that failed this round.

        Returns:
            Tuple of (aggregated Parameters, metrics dict).
        """
        if not results:
            return None, {}

        if failures:
            logger.warning(
                "Round %d: %d clients failed", server_round, len(failures)
            )

        start_time = time.time()

        if self.he_enabled and self.context is not None:
            result = self._aggregate_encrypted(server_round, results)
        else:
            logger.info(
                "HE disabled — falling back to plaintext FedAvg (round %d)",
                server_round,
            )
            result = super().aggregate_fit(server_round, results, failures)

        elapsed = time.time() - start_time
        logger.info(
            "Round %d aggregation complete in %.2fs (HE=%s)",
            server_round,
            elapsed,
            self.he_enabled,
        )
        return result

    def _aggregate_encrypted(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        """
        Perform HE aggregation over CKKS-encrypted client weights.

        Args:
            server_round: Current round number.
            results: List of (client, FitRes) from clients.

        Returns:
            Aggregated plaintext Parameters and metrics.
        """
        client_ciphertexts = []
        client_sample_counts = []
        client_metrics = []
        shapes_ref = None

        for client_proxy, fit_res in results:
            ndarrays = parameters_to_ndarrays(fit_res.parameters)

            if len(ndarrays) < 2:
                logger.warning(
                    "Client %s: unexpected NDArray count %d, skipping",
                    client_proxy.cid,
                    len(ndarrays),
                )
                continue

            shapes_arr = ndarrays[-1]
            ct_arrays = ndarrays[:-1]

            if shapes_ref is None:
                shapes_ref = [
                    tuple(int(x) for x in row) for row in shapes_arr
                ]

            ct_bytes_list = [
                ndarray_to_ciphertexts(ct_arr) for ct_arr in ct_arrays
            ]
            flat_ct_list = [item for sublist in ct_bytes_list for item in sublist]

            client_ciphertexts.append(flat_ct_list)
            client_sample_counts.append(float(fit_res.num_examples))
            client_metrics.append(fit_res.metrics or {})

        if not client_ciphertexts:
            logger.error("No valid encrypted weights received in round %d", server_round)
            return None, {}

        logger.info(
            "Round %d: Aggregating ciphertexts from %d clients",
            server_round,
            len(client_ciphertexts),
        )

        agg_ciphertexts = aggregate_encrypted_weights(
            client_ciphertexts,
            client_sample_counts,
            self.context,
        )

        if shapes_ref is None:
            logger.error("Cannot determine weight shapes — missing shape metadata")
            return None, {}

        decrypted = decrypt_weights(agg_ciphertexts, shapes_ref, self.context)

        dice_scores = [m.get("dice", 0.0) for m in client_metrics if "dice" in m]
        mean_dice = float(np.mean(dice_scores)) if dice_scores else 0.0

        metrics = {
            "round": server_round,
            "clients": len(client_ciphertexts),
            "dice": mean_dice,
            "he_enabled": True,
        }

        self.round_metrics.append(metrics)
        logger.info(
            "Round %d decrypted successfully. Mean client Dice: %.4f",
            server_round,
            mean_dice,
        )

        return ndarrays_to_parameters(decrypted), metrics


def get_he_strategy(model_params: Parameters) -> HEFedAvgStrategy:
    """
    Build the HE-enabled strategy with initial model parameters.

    Args:
        model_params: Initial global model parameters.

    Returns:
        Configured HEFedAvgStrategy instance.
    """
    return HEFedAvgStrategy(
        context_path=CONTEXT_PATH,
        he_enabled=HE_ENABLED,
        proximal_mu=0.01,
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=MIN_CLIENTS,
        min_evaluate_clients=MIN_CLIENTS,
        min_available_clients=MIN_CLIENTS,
        initial_parameters=model_params,
    )


def start_he_server(initial_parameters: Parameters) -> None:
    """
    Start the HE-enabled federated learning server.

    Args:
        initial_parameters: Initial global model parameters to broadcast
            to clients at the start of training.
    """
    strategy = get_he_strategy(initial_parameters)
    he_status = "ENABLED (CKKS 128-bit)" if HE_ENABLED else "DISABLED (plaintext)"

    logger.info("FedMed FL Server v3 starting")
    logger.info("  Address: %s", SERVER_ADDRESS)
    logger.info("  Rounds:  %d", ROUNDS)
    logger.info("  Clients: min %d", MIN_CLIENTS)
    logger.info("  HE Mode: %s", he_status)

    fl.server.start_server(
        server_address=SERVER_ADDRESS,
        config=fl.server.ServerConfig(num_rounds=ROUNDS),
        strategy=strategy,
    )
