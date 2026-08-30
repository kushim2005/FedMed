"""
Member 2 - ML Engineer
Task: Evaluation Metrics for Segmentation
Day 4-5: Dice Score, Hausdorff Distance, and baseline report
"""

import torch
import numpy as np
from typing import Dict, List
from monai.metrics import DiceMetric, HausdorffDistanceMetric
from monai.transforms import AsDiscrete
from monai.utils.enums import MetricReduction


# BraTS 2021 tumor sub-regions
REGION_NAMES = {
    0: "Background",
    1: "Necrotic Core (NCR)",
    2: "Peritumoral Edema (ED)",
    3: "Enhancing Tumor (ET)",
}

# Clinical composite regions
WHOLE_TUMOR_CLASSES = [1, 2, 3]    # WT = all tumor regions
TUMOR_CORE_CLASSES = [1, 3]        # TC = NCR + ET
ENHANCING_TUMOR_CLASSES = [3]      # ET = enhancing tumor only


class SegmentationEvaluator:
    """
    Computes segmentation metrics for BraTS 2021 predictions.

    Metrics:
        - Dice Score (per class + composite regions)
        - Hausdorff Distance 95th percentile
    """

    def __init__(self, num_classes: int = 4, device: str = "cpu"):
        self.num_classes = num_classes
        self.device = device

        # MONAI Dice metric
        self.dice_metric = DiceMetric(
            include_background=False,
            reduction=MetricReduction.MEAN_BATCH,
            get_not_nans=True,
        )

        # MONAI Hausdorff metric (95th percentile)
        self.hd95_metric = HausdorffDistanceMetric(
            include_background=False,
            percentile=95,
            reduction=MetricReduction.MEAN_BATCH,
        )

        # Convert logits to one-hot predictions
        self.post_pred = AsDiscrete(argmax=True, to_onehot=num_classes)
        self.post_label = AsDiscrete(to_onehot=num_classes)

    def update(self, outputs: torch.Tensor, labels: torch.Tensor):
        """
        Update metrics with a batch of predictions.
        Args:
            outputs: Model logits (B, C, H, W, D)
            labels:  Ground truth (B, 1, H, W, D)
        """
        outputs_onehot = torch.stack([self.post_pred(o) for o in outputs])
        labels_onehot = torch.stack([self.post_label(l) for l in labels])

        self.dice_metric(y_pred=outputs_onehot, y=labels_onehot)
        self.hd95_metric(y_pred=outputs_onehot, y=labels_onehot)

    def compute(self) -> Dict[str, float]:
        """
        Compute and return all metrics.
        Returns dict with Dice and HD95 per class and per composite region.
        """
        dice_per_class, _ = self.dice_metric.aggregate()
        hd95_per_class, _ = self.hd95_metric.aggregate()

        results = {}

        # Per-class Dice
        for i, name in REGION_NAMES.items():
            if i > 0:  # Skip background
                results[f"Dice_{name}"] = dice_per_class[i - 1].item()

        # Composite region Dice
        results["Dice_WT"] = dice_per_class[[0, 1, 2]].mean().item()   # Whole Tumor
        results["Dice_TC"] = dice_per_class[[0, 2]].mean().item()       # Tumor Core
        results["Dice_ET"] = dice_per_class[2].item()                   # Enhancing Tumor
        results["Dice_Mean"] = dice_per_class.mean().item()

        # HD95
        results["HD95_Mean"] = hd95_per_class.mean().item()

        return results

    def reset(self):
        """Reset metrics for next epoch."""
        self.dice_metric.reset()
        self.hd95_metric.reset()


def compute_dice_score(outputs: torch.Tensor, labels: torch.Tensor) -> float:
    """
    Quick single-batch Dice computation (used during FL training).
    Args:
        outputs: Model logits (B, C, H, W, D)
        labels:  Ground truth (B, 1, H, W, D)
    Returns:
        Mean Dice score as float
    """
    post_pred = AsDiscrete(argmax=True, to_onehot=4)
    post_label = AsDiscrete(to_onehot=4)
    dice_metric = DiceMetric(include_background=False, reduction=MetricReduction.MEAN)

    outputs_onehot = torch.stack([post_pred(o) for o in outputs])
    labels_onehot = torch.stack([post_label(l) for l in labels])

    dice_metric(y_pred=outputs_onehot, y=labels_onehot)
    result, _ = dice_metric.aggregate()
    return result.item()


def print_baseline_report(metrics: Dict[str, float], epoch: int):
    """Prints a formatted baseline metrics report."""
    print("\n" + "=" * 55)
    print(f"  FedMed Baseline Report — Epoch {epoch}")
    print("=" * 55)
    print(f"  Dice (Whole Tumor):      {metrics.get('Dice_WT', 0):.4f}")
    print(f"  Dice (Tumor Core):       {metrics.get('Dice_TC', 0):.4f}")
    print(f"  Dice (Enhancing Tumor):  {metrics.get('Dice_ET', 0):.4f}")
    print(f"  Dice (Mean):             {metrics.get('Dice_Mean', 0):.4f}")
    print(f"  HD95 (Mean):             {metrics.get('HD95_Mean', 0):.2f} mm")
    print("=" * 55 + "\n")
