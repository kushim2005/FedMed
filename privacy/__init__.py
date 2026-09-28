"""FedMed Privacy Module — Differential Privacy via DP-SGD (Opacus)."""

from privacy.privacy_budget import PrivacyBudget
from privacy.dp_trainer import DPTrainer

__all__ = ["PrivacyBudget", "DPTrainer"]
