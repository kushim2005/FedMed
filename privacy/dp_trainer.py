"""
privacy/dp_trainer.py
FedMed — Differentially Private Training with Opacus DP-SGD.

Author: Ravi (Integration Lead)
Week 4: DP-SGD Training Wrapper

Wraps PyTorch model training with Opacus PrivacyEngine to implement
DP-SGD (Differentially Private Stochastic Gradient Descent):
  1. Per-sample gradient clipping (max L2 norm = C)
  2. Calibrated Gaussian noise addition (σ = noise_multiplier * C)
  3. Rényi DP accounting to track (ε, δ)-DP guarantee

Reference: Abadi et al. 2016 — "Deep Learning with Differential Privacy"
Accounting: Mironov 2017 — "Rényi Differential Privacy"
"""

import logging
import os
from typing import Optional, Tuple

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

logger = logging.getLogger(__name__)

try:
    from opacus import PrivacyEngine
    from opacus.validators import ModuleValidator
    OPACUS_AVAILABLE = True
except ImportError:
    OPACUS_AVAILABLE = False

DP_ENABLED = os.environ.get("DP_ENABLED", "true").lower() == "true"
NOISE_MULTIPLIER = float(os.environ.get("NOISE_MULTIPLIER", "1.1"))
MAX_GRAD_NORM = float(os.environ.get("MAX_GRAD_NORM", "1.0"))
TARGET_DELTA = float(os.environ.get("TARGET_DELTA", "1e-5"))
MAX_EPSILON = float(os.environ.get("MAX_EPSILON", "3.5"))


class DPTrainer:
    """
    Differentially Private training wrapper using Opacus DP-SGD.

    Attaches an Opacus PrivacyEngine to a PyTorch model + optimizer,
    enabling per-sample gradient clipping and calibrated Gaussian noise.
    Tracks cumulative privacy expenditure across training steps.

    Attributes:
        model: The wrapped PyTorch model (GradSampleModule after attach).
        optimizer: DP-enabled optimizer with per-sample gradient computation.
        privacy_engine: Opacus PrivacyEngine managing noise + accounting.
        noise_multiplier: Gaussian noise scale (σ relative to clip norm).
        max_grad_norm: Per-sample gradient clipping bound (C).
        delta: Target delta for (ε, δ)-DP guarantee.
        enabled: Whether DP-SGD is active (fallback to standard SGD if False).
    """

    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        data_loader: DataLoader,
        noise_multiplier: float = NOISE_MULTIPLIER,
        max_grad_norm: float = MAX_GRAD_NORM,
        delta: float = TARGET_DELTA,
        max_epsilon: float = MAX_EPSILON,
        enabled: bool = DP_ENABLED,
    ):
        """
        Initialize the DPTrainer and optionally attach Opacus PrivacyEngine.

        Args:
            model: PyTorch model to train with DP-SGD.
            optimizer: Optimizer (Adam, SGD) — will be wrapped by Opacus.
            data_loader: Training DataLoader (batch_size must be consistent).
            noise_multiplier: Ratio σ/C for Gaussian noise. Higher values
                give stronger privacy but reduce accuracy. Default 1.1
                gives ε≈2.8 at δ=1e-5 for 10 rounds (n=100).
            max_grad_norm: Per-sample gradient clipping norm (C). Default 1.0
                covers 95% of gradient norms for FedMed 3D U-Net.
            delta: Privacy failure probability. Default 1e-5.
            max_epsilon: Budget cap; training should stop above this. Default 3.5.
            enabled: Activate DP-SGD. If False, standard training is used.
        """
        self.noise_multiplier = noise_multiplier
        self.max_grad_norm = max_grad_norm
        self.delta = delta
        self.max_epsilon = max_epsilon
        self.enabled = enabled
        self.privacy_engine: Optional[PrivacyEngine] = None

        if self.enabled and OPACUS_AVAILABLE:
            model = self._fix_incompatible_layers(model)
            self.model, self.optimizer, self.data_loader = self._attach(
                model, optimizer, data_loader
            )
        else:
            self.model = model
            self.optimizer = optimizer
            self.data_loader = data_loader

            if self.enabled and not OPACUS_AVAILABLE:
                logger.warning(
                    "DP requested but Opacus not installed — "
                    "falling back to standard SGD. pip install opacus"
                )
                self.enabled = False

    @staticmethod
    def _fix_incompatible_layers(model: nn.Module) -> nn.Module:
        """
        Replace Opacus-incompatible layers (e.g., BatchNorm) with DP-compatible
        equivalents (GroupNorm). Opacus requires per-sample gradient computation,
        which BatchNorm does not support.

        Args:
            model: Original PyTorch model.

        Returns:
            Opacus-compatible model with BatchNorm replaced by GroupNorm.
        """
        if not OPACUS_AVAILABLE:
            return model

        errors = ModuleValidator.validate(model, strict=False)
        if errors:
            logger.info(
                "Fixing %d Opacus-incompatible layer(s): %s",
                len(errors),
                [type(e).__name__ for e in errors],
            )
            model = ModuleValidator.fix(model)

        return model

    def _attach(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        data_loader: DataLoader,
    ) -> Tuple[nn.Module, torch.optim.Optimizer, DataLoader]:
        """
        Attach Opacus PrivacyEngine to model, optimizer, and data loader.

        Args:
            model: Compatible PyTorch model.
            optimizer: Standard PyTorch optimizer.
            data_loader: Training DataLoader.

        Returns:
            Tuple of (dp_model, dp_optimizer, dp_data_loader).
        """
        self.privacy_engine = PrivacyEngine()

        dp_model, dp_optimizer, dp_loader = self.privacy_engine.make_private(
            module=model,
            optimizer=optimizer,
            data_loader=data_loader,
            noise_multiplier=self.noise_multiplier,
            max_grad_norm=self.max_grad_norm,
            poisson_sampling=True,
        )

        logger.info(
            "PrivacyEngine attached: σ=%.2f, C=%.1f, δ=%.1e, max_ε=%.1f",
            self.noise_multiplier,
            self.max_grad_norm,
            self.delta,
            self.max_epsilon,
        )
        return dp_model, dp_optimizer, dp_loader

    def get_privacy_spent(self) -> Tuple[float, float]:
        """
        Query the current accumulated (ε, δ)-DP privacy expenditure.

        Returns:
            Tuple (epsilon, delta). Returns (inf, delta) if Opacus
            is not available or DP is disabled.
        """
        if not self.enabled or self.privacy_engine is None:
            return float("inf"), self.delta

        epsilon = self.privacy_engine.get_epsilon(delta=self.delta)
        return float(epsilon), self.delta

    def is_budget_exceeded(self) -> bool:
        """
        Check if training has exceeded the configured epsilon budget.

        Returns:
            True if current ε > max_epsilon, False otherwise.
        """
        epsilon, _ = self.get_privacy_spent()
        exceeded = epsilon > self.max_epsilon

        if exceeded:
            logger.warning(
                "Privacy budget exceeded: ε=%.4f > max_ε=%.1f — "
                "training should stop to maintain privacy guarantee",
                epsilon,
                self.max_epsilon,
            )
        return exceeded

    def train_one_epoch(
        self,
        criterion: nn.Module,
        device: torch.device,
        proximal_mu: float = 0.01,
        global_params: Optional[list] = None,
    ) -> Tuple[float, float]:
        """
        Train the model for one epoch using DP-SGD.

        Includes FedProx proximal term to regularize distance from the
        global model, identical to non-DP training (Week 2).

        Args:
            criterion: Loss function (e.g., DiceCELoss).
            device: PyTorch device.
            proximal_mu: FedProx proximal coefficient.
            global_params: List of global model parameter tensors
                for proximal regularization. None = no proximal term.

        Returns:
            Tuple (average_loss, epsilon) for this epoch.
        """
        self.model.train()
        total_loss = 0.0
        num_batches = 0

        for batch in self.data_loader:
            images = batch["image"].to(device)
            labels = batch["label"].to(device)

            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = criterion(outputs, labels)

            if global_params is not None:
                prox = sum(
                    (mu / 2.0) * torch.norm(p - g) ** 2
                    for p, g in zip(self.model.parameters(), global_params)
                    for mu in [proximal_mu]
                )
                loss = loss + prox

            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()
            num_batches += 1

            if self.is_budget_exceeded():
                logger.warning(
                    "Budget exceeded mid-epoch — stopping epoch early"
                )
                break

        avg_loss = total_loss / max(num_batches, 1)
        epsilon, _ = self.get_privacy_spent()

        logger.info(
            "Epoch complete: loss=%.4f, ε=%.4f (DP=%s)",
            avg_loss,
            epsilon,
            self.enabled,
        )
        return avg_loss, epsilon

    def log_privacy_status(self, round_id: int) -> None:
        """
        Log the current privacy status for the given FL round.

        Args:
            round_id: Current FL round number.
        """
        epsilon, delta = self.get_privacy_spent()
        pct = min(100.0, 100 * epsilon / self.max_epsilon)

        logger.info(
            "Round %d privacy status: ε=%.4f, δ=%.1e, budget used: %.1f%%",
            round_id,
            epsilon,
            delta,
            pct,
        )
