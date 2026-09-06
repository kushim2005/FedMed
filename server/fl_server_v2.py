"""
server/fl_server_v2.py
Member 3 - Kushi (FL Systems Lead)
Week 2: Enhanced Federated Learning Server with TLS gRPC & FedProx / FedAvg.

Features:
- Encrypted gRPC channel via mutual/server TLS credentials.
- Configurable FedProx (with proximal term mu) and standard FedAvg strategies.
- Fault tolerance: training proceeds with min_available_clients (e.g. 2 of 3).
- Model checkpointing per N rounds to checkpoints/ directory.
- Background health check endpoint on port 8090.
"""

import os
import sys
import json
import argparse
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import torch
import flwr as fl
from flwr.common import Metrics, Parameters, Scalar, parameters_to_ndarrays, ndarrays_to_parameters
from flwr.server.strategy import FedAvg, FedProx

sys.path.append(str(Path(__file__).parent.parent.resolve()))
from model.unet3d import build_model
from utils.logger import get_logger
from security.tls_config import load_server_credentials, certs_exist

logger = get_logger("FedMedServerV2")
CURRENT_ROUND = 0


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = {"status": "healthy", "service": "FedMedServerV2", "round": CURRENT_ROUND}
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Quiet logging for health probes


def start_health_server(port: int = 8090):
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Health-check endpoint active on port {port} (/health)")


def weighted_average_metrics(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    """Aggregate per-hospital evaluation metrics weighted by sample count."""
    total_examples = sum(num_examples for num_examples, _ in metrics)
    if total_examples == 0:
        return {"dice_score": 0.0}

    weighted_dice = sum(
        num_examples * float(m.get("dice_score", 0.0)) for num_examples, m in metrics
    )
    return {"dice_score": weighted_dice / total_examples}


class FedMedAggregateStrategy(FedProx):
    """
    Custom strategy that inherits from FedProx with automatic checkpointing,
    per-round metric logging, and fault-tolerant client aggregation.
    """

    def __init__(
        self,
        checkpoint_dir: str = "checkpoints",
        checkpoint_interval: int = 5,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_interval = checkpoint_interval
        self.round_history: List[Dict[str, Union[int, float]]] = []

    def aggregate_fit(
        self,
        server_round: int,
        results,
        failures,
    ):
        global CURRENT_ROUND
        CURRENT_ROUND = server_round
        logger.info(
            f"--- Round {server_round} Aggregation: "
            f"{len(results)} client(s) succeeded, {len(failures)} failed ---"
        )
        aggregated_parameters, aggregated_metrics = super().aggregate_fit(
            server_round, results, failures
        )

        if aggregated_parameters is not None:
            if server_round % self.checkpoint_interval == 0:
                self._save_checkpoint(server_round, aggregated_parameters)

        return aggregated_parameters, aggregated_metrics

    def aggregate_evaluate(
        self,
        server_round: int,
        results,
        failures,
    ):
        loss, metrics = super().aggregate_evaluate(server_round, results, failures)
        dice = metrics.get("dice_score", 0.0) if metrics else 0.0
        logger.info(f"Round {server_round} Evaluation -> Loss: {loss:.4f}, Dice: {dice:.4f}")
        self.round_history.append({"round": server_round, "loss": loss, "dice_score": dice})

        results_dir = Path("results")
        results_dir.mkdir(parents=True, exist_ok=True)
        with open(results_dir / "server_round_metrics.json", "w", encoding="utf-8") as f:
            json.dump(self.round_history, f, indent=2)

        return loss, metrics

    def _save_checkpoint(self, server_round: int, parameters: Parameters):
        ckpt_path = self.checkpoint_dir / f"global_model_round_{server_round}.pt"
        ndarrays = parameters_to_ndarrays(parameters)
        temp_model = build_model("cpu")
        params_dict = zip(temp_model.state_dict().keys(), ndarrays)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        torch.save(state_dict, ckpt_path)
        logger.info(f"Saved global model checkpoint: {ckpt_path}")


def main():
    parser = argparse.ArgumentParser(description="FedMed Server V2")
    parser.add_argument("--rounds", type=int, default=10, help="Number of FL rounds")
    parser.add_argument("--port", type=int, default=8080, help="gRPC port")
    parser.add_argument("--health-port", type=int, default=8090, help="Health check port")
    parser.add_argument("--mu", type=float, default=0.1, help="FedProx proximal term mu")
    parser.add_argument("--no-tls", action="store_true", help="Disable TLS for local debugging")
    args = parser.parse_args()

    start_health_server(args.health_port)

    # Initial model parameters
    initial_model = build_model("cpu")
    initial_weights = [val.cpu().numpy() for _, val in initial_model.state_dict().items()]
    initial_parameters = ndarrays_to_parameters(initial_weights)

    strategy = FedMedAggregateStrategy(
        proximal_mu=args.mu,
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=2,
        min_evaluate_clients=2,
        min_available_clients=2,
        evaluate_metrics_aggregation_fn=weighted_average_metrics,
        initial_parameters=initial_parameters,
    )

    use_tls = not args.no_tls and certs_exist()
    server_address = f"0.0.0.0:{args.port}"

    if use_tls:
        logger.info(f"Starting TLS-secured Flower FL Server on {server_address}...")
        certs = load_server_credentials()
        fl.server.start_server(
            server_address=server_address,
            config=fl.server.ServerConfig(num_rounds=args.rounds),
            strategy=strategy,
            certificates=certs,
        )
    else:
        logger.warning(f"Starting INSECURE Flower FL Server (no TLS) on {server_address}...")
        fl.server.start_server(
            server_address=server_address,
            config=fl.server.ServerConfig(num_rounds=args.rounds),
            strategy=strategy,
        )


if __name__ == "__main__":
    main()
