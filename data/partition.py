"""
data/partition.py
Member 1 - Ravi (Data Integration & Testing Lead)
Week 2: Dirichlet-based Non-IID Dataset Partitioning for BraTS 2021.

This module partitions the dataset across N hospital nodes (default: 3)
using a Dirichlet distribution to simulate statistical heterogeneity (non-IID).
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np


class DirichletPartitioner:
    """
    Partitions dataset sample indices among multiple hospital silos
    according to a Dirichlet distribution Dir(alpha).
    """

    def __init__(self, num_clients: int = 3, alpha: float = 0.5, seed: int = 42):
        self.num_clients = num_clients
        self.alpha = alpha
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def partition_indices(self, total_samples: int) -> Dict[int, List[int]]:
        """
        Split range(total_samples) across clients with proportions drawn from Dir(alpha).
        Ensures each client receives at least one sample.
        """
        if total_samples < self.num_clients:
            raise ValueError(
                f"total_samples ({total_samples}) must be >= num_clients ({self.num_clients})"
            )

        indices = np.arange(total_samples)
        self.rng.shuffle(indices)

        proportions = self.rng.dirichlet(np.repeat(self.alpha, self.num_clients))
        counts = np.maximum(1, np.round(proportions * total_samples).astype(int))

        # Adjust total sum to match total_samples exactly
        diff = total_samples - counts.sum()
        if diff != 0:
            idx = np.argmax(counts) if diff < 0 else np.argmin(counts)
            counts[idx] += diff

        splits = np.split(indices, np.cumsum(counts)[:-1])
        return {client_id + 1: split.tolist() for client_id, split in enumerate(splits)}


def partition_brats_dataset(
    data_dir: str,
    output_json: Optional[str] = None,
    num_clients: int = 3,
    alpha: float = 0.5,
    seed: int = 42,
) -> Dict[int, List[str]]:
    """
    Discover all BraTS patient cases in data_dir, partition them across hospital nodes,
    and optionally save the partition map to a JSON file.
    """
    path = Path(data_dir)
    if not path.exists():
        # Fallback to mock patient IDs if dataset directory does not exist yet
        case_names = [f"BraTS2021_{i:05d}" for i in range(1, 370)]
    else:
        case_dirs = sorted([d.name for d in path.iterdir() if d.is_dir() and any(d.iterdir())])
        case_names = case_dirs if case_dirs else [f"BraTS2021_{i:05d}" for i in range(1, 370)]

    partitioner = DirichletPartitioner(num_clients=num_clients, alpha=alpha, seed=seed)
    index_map = partitioner.partition_indices(len(case_names))

    named_map: Dict[int, List[str]] = {}
    for client_id, idxs in index_map.items():
        named_map[client_id] = [case_names[i] for i in idxs]

    if output_json:
        out_p = Path(output_json)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(named_map, f, indent=2)

    return named_map


def load_partition_map(json_path: str) -> Dict[int, List[str]]:
    """Load pre-computed partition map from JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {int(k): v for k, v in data.items()}
