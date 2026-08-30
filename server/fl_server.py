"""
Member 3 - FL Systems Lead
Task: Flower FL Server with FedProx Strategy
Day 1-5: Orchestrate decentralized training loop across 3 hospital nodes
"""

import sys
import os
from typing import List, Tuple, Optional, Dict
from collections import OrderedDict

import flwr as fl
from flwr.common import Metrics, FitIns, EvaluateIns
import numpy as np
import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.unet3d import build_model
from utils.logger import get_logger

logger = get_logger("FedMedServer")


def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    """
    Aggregation function for evaluation metrics.
    Computes weighted average of Dice scores across all hospital nodes.

    Args:
        metrics: List of (num_examples, metrics_dict) from each client

    Returns:
        Dict with aggregated metrics
    """
    total_examples = sum(num for num, _ in metrics)

    # Weighted average of Dice scores
    dice_scores = [num * m.get("dice_score", 0.0) for num, m in metrics]
    weighted_dice = sum(dice_scores) / total_examples if total_examples > 0 else 0.0

    return {
        "dice_score": weighted_dice,
        "total_examples": total_examples,
    }


def get_evaluate_fn(device: str = "cpu"):
    """
    Returns server-side evaluation function.
    Evaluates the global model on a shared validation set.
    """
    def evaluate(
        server_round: int,
        parameters: fl.common.NDArrays,
        config: Dict,
    ) -> Optional[Tuple[float, Dict]]:

        model = build_model(device)

        # Load aggregated weights into model
        params_dict = zip(model.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        model.load_state_dict(state_dict, strict=True)
        model.eval()

        # Log server round
        logger.info(f"[Server] Round {server_round} — Global model evaluation")

        # Return placeholder loss (real validation requires data at server)
        return 0.0, {"round": server_round}

    return evaluate


def fit_config(server_round: int) -> Dict:
    """
    Returns training config sent to clients each round.
    Config can vary per round (e.g., more epochs early, fewer later).
    """
    return {
        "server_round": server_round,
        "local_epochs": 3 if server_round <= 10 else 2,
        "batch_size": 1,
        "learning_rate": 1e-4,
    }


def evaluate_config(server_round: int) -> Dict:
    """Returns evaluation config sent to clients."""
    return {"server_round": server_round}


def create_fedprox_strategy(initial_model) -> fl.server.strategy.FedProx:
    """
    Creates FedProx strategy — better than FedAvg for non-IID hospital data.

    FedProx adds a proximal term to each client's loss:
        L_client = L_local + (mu/2) * ||w - w_global||^2

    This prevents clients with very different data from diverging too far.
    """
    # Get initial model weights as numpy arrays
    initial_parameters = fl.common.ndarrays_to_parameters(
        [val.cpu().numpy() for _, val in initial_model.state_dict().items()]
    )

    strategy = fl.server.strategy.FedProx(
        proximal_mu=0.1,                     # Proximal term strength
        fraction_fit=1.0,                    # Use ALL clients each round
        fraction_evaluate=1.0,               # Evaluate ALL clients each round
        min_fit_clients=2,                   # Minimum clients to proceed with round
        min_evaluate_clients=2,
        min_available_clients=2,             # Wait for at least 2 hospitals
        evaluate_fn=get_evaluate_fn(),       # Server-side evaluation
        on_fit_config_fn=fit_config,         # Send config to clients
        on_evaluate_config_fn=evaluate_config,
        evaluate_metrics_aggregation_fn=weighted_average,
        initial_parameters=initial_parameters,
    )

    return strategy


def start_server(
    server_address: str = "0.0.0.0:8080",
    num_rounds: int = 50,
):
    """
    Start the FedMed FL server.

    Args:
        server_address: Host:port to listen on
        num_rounds: Number of federated learning rounds
    """
    logger.info("=" * 50)
    logger.info("  FedMed FL Server Starting")
    logger.info(f"  Address:    {server_address}")
    logger.info(f"  FL Rounds:  {num_rounds}")
    logger.info(f"  Strategy:   FedProx (mu=0.1)")
    logger.info("=" * 50)

    # Initialize global model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    global_model = build_model(device)

    # Create FedProx strategy
    strategy = create_fedprox_strategy(global_model)

    # Start Flower server
    history = fl.server.start_server(
        server_address=server_address,
        config=fl.server.ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
    )

    logger.info("FL Training Complete!")
    logger.info(f"Final losses: {history.losses_distributed}")
    return history


if __name__ == "__main__":
    start_server(
        server_address="0.0.0.0:8080",
        num_rounds=50,
    )
