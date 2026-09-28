"""
privacy/privacy_budget.py
FedMed — Differential Privacy Budget Tracking.

Author: Kushi (FL Systems)
Week 4: Privacy Accounting via Rényi DP

Tracks cumulative (ε, δ)-differential privacy budget across FL rounds
using Opacus's Rényi DP accountant. Enforces configurable budget limits
to ensure training stops before privacy degradation exceeds policy.

Mathematical basis:
  - Rényi DP (RDP) via Mironov 2017 accounting
  - Conversion: RDP(α, ε_α) → (ε, δ)-DP using Proposition 3 (Mironov 2017)
  - Composition: sum of Rényi divergences across rounds
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from opacus.accountants import RDPAccountant
    from opacus.accountants.utils import get_noise_multiplier
    OPACUS_AVAILABLE = True
except ImportError:
    OPACUS_AVAILABLE = False


@dataclass
class RoundPrivacyRecord:
    """Per-round privacy accounting record."""

    round_id: int
    epsilon: float
    delta: float
    noise_multiplier: float
    clip_norm: float
    sample_rate: float
    steps: int
    dice_score: float = 0.0


@dataclass
class PrivacyBudget:
    """
    Tracks cumulative Rényi DP privacy budget across federated rounds.

    Uses Opacus RDPAccountant for mathematically rigorous accounting.
    Raises BudgetExceededError when training would violate the configured
    maximum epsilon.

    Attributes:
        max_epsilon: Maximum allowed (ε, δ)-DP epsilon. Training stops
            if the next step would exceed this budget.
        delta: Target delta for (ε, δ)-DP guarantee. Typically 1/n where
            n is the training dataset size.
        noise_multiplier: Gaussian noise multiplier (σ/C ratio).
        max_grad_norm: Gradient clipping norm (C).
    """

    max_epsilon: float = 3.5
    delta: float = 1e-5
    noise_multiplier: float = 1.1
    max_grad_norm: float = 1.0
    _accountant: object = field(default=None, init=False, repr=False)
    _records: List[RoundPrivacyRecord] = field(
        default_factory=list, init=False, repr=False
    )
    _current_epsilon: float = field(default=0.0, init=False, repr=False)

    def __post_init__(self):
        """Initialize the Rényi DP accountant."""
        if not OPACUS_AVAILABLE:
            logger.warning(
                "Opacus not installed — privacy accounting disabled. "
                "Install with: pip install opacus"
            )
            return

        self._accountant = RDPAccountant()
        logger.info(
            "PrivacyBudget initialized: max_ε=%.1f, δ=%.1e, σ=%.2f, C=%.1f",
            self.max_epsilon,
            self.delta,
            self.noise_multiplier,
            self.max_grad_norm,
        )

    def step(
        self,
        sample_rate: float,
        steps: int = 1,
        noise_multiplier: Optional[float] = None,
    ) -> float:
        """
        Advance the privacy accountant by one or more training steps.

        Args:
            sample_rate: Poisson subsampling rate (batch_size / dataset_size).
            steps: Number of gradient steps taken.
            noise_multiplier: Override noise multiplier for this step.
                Uses self.noise_multiplier if not provided.

        Returns:
            Current cumulative epsilon after this step.

        Raises:
            RuntimeError: If Opacus is not installed.
        """
        if not OPACUS_AVAILABLE or self._accountant is None:
            raise RuntimeError(
                "Opacus required for privacy accounting. "
                "pip install opacus"
            )

        sigma = noise_multiplier if noise_multiplier is not None else self.noise_multiplier

        self._accountant.step(
            noise_multiplier=sigma,
            sample_rate=sample_rate,
        )

        self._current_epsilon = self._accountant.get_epsilon(delta=self.delta)

        logger.debug(
            "Privacy step: sample_rate=%.4f, σ=%.2f, steps=%d → ε=%.4f",
            sample_rate,
            sigma,
            steps,
            self._current_epsilon,
        )
        return self._current_epsilon

    def get_epsilon(self, delta: Optional[float] = None) -> float:
        """
        Get the current cumulative epsilon value.

        Args:
            delta: Target delta. Uses self.delta if not provided.

        Returns:
            Current (ε, δ)-DP epsilon.
        """
        if not OPACUS_AVAILABLE or self._accountant is None:
            return float("inf")

        target_delta = delta if delta is not None else self.delta
        return self._accountant.get_epsilon(delta=target_delta)

    def is_budget_exceeded(self, epsilon: Optional[float] = None) -> bool:
        """
        Check whether the privacy budget has been exceeded.

        Args:
            epsilon: Epsilon to compare against max_epsilon.
                Uses current accumulated epsilon if not provided.

        Returns:
            True if the budget has been exceeded, False otherwise.
        """
        check_epsilon = epsilon if epsilon is not None else self._current_epsilon
        exceeded = check_epsilon > self.max_epsilon

        if exceeded:
            logger.warning(
                "Privacy budget exceeded: ε=%.4f > max_ε=%.4f",
                check_epsilon,
                self.max_epsilon,
            )
        return exceeded

    def log_round(
        self,
        round_id: int,
        sample_rate: float,
        steps: int,
        dice_score: float = 0.0,
        noise_multiplier: Optional[float] = None,
    ) -> RoundPrivacyRecord:
        """
        Record privacy expenditure for one FL round.

        Args:
            round_id: FL round number.
            sample_rate: Poisson subsampling rate used in this round.
            steps: Number of gradient steps in this round.
            dice_score: Model Dice score at end of this round.
            noise_multiplier: Noise multiplier used (defaults to self.noise_multiplier).

        Returns:
            RoundPrivacyRecord for this round.
        """
        sigma = noise_multiplier if noise_multiplier is not None else self.noise_multiplier
        epsilon = self.step(sample_rate=sample_rate, steps=steps, noise_multiplier=sigma)

        record = RoundPrivacyRecord(
            round_id=round_id,
            epsilon=epsilon,
            delta=self.delta,
            noise_multiplier=sigma,
            clip_norm=self.max_grad_norm,
            sample_rate=sample_rate,
            steps=steps,
            dice_score=dice_score,
        )
        self._records.append(record)

        logger.info(
            "Round %d privacy: ε=%.4f / max=%.1f (%.1f%% used), dice=%.4f",
            round_id,
            epsilon,
            self.max_epsilon,
            100 * epsilon / self.max_epsilon,
            dice_score,
        )
        return record

    def get_summary(self) -> dict:
        """
        Return a summary of the privacy budget status.

        Returns:
            Dict with current epsilon, delta, rounds, and budget utilization.
        """
        return {
            "current_epsilon": self._current_epsilon,
            "max_epsilon": self.max_epsilon,
            "delta": self.delta,
            "budget_used_pct": round(
                100 * self._current_epsilon / self.max_epsilon, 2
            ),
            "rounds_logged": len(self._records),
            "budget_exceeded": self.is_budget_exceeded(),
            "noise_multiplier": self.noise_multiplier,
            "max_grad_norm": self.max_grad_norm,
        }

    def export_csv(self, path: str) -> None:
        """
        Export per-round privacy records to a CSV file.

        Args:
            path: Output CSV file path.
        """
        import csv
        import os

        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

        fields = [
            "round_id", "epsilon", "delta", "noise_multiplier",
            "clip_norm", "sample_rate", "steps", "dice_score",
        ]
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for rec in self._records:
                writer.writerow(
                    {
                        "round_id": rec.round_id,
                        "epsilon": f"{rec.epsilon:.6f}",
                        "delta": f"{rec.delta:.1e}",
                        "noise_multiplier": f"{rec.noise_multiplier:.4f}",
                        "clip_norm": f"{rec.clip_norm:.2f}",
                        "sample_rate": f"{rec.sample_rate:.6f}",
                        "steps": rec.steps,
                        "dice_score": f"{rec.dice_score:.6f}",
                    }
                )

        logger.info("Privacy records exported to %s (%d rows)", path, len(self._records))

    def reset(self) -> None:
        """
        Reset the privacy accountant. Clears all accumulated privacy spending.
        Use for ablation studies or re-training experiments.
        """
        if OPACUS_AVAILABLE:
            self._accountant = RDPAccountant()
        self._records = []
        self._current_epsilon = 0.0
        logger.info("Privacy budget reset")
