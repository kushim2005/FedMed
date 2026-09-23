"""
eval/federated_metrics.py
Member 2 - Ranjith Kumar (ML Engineer)
Week 2: Per-Round Federated Metrics Tracking & Visualization.

Tracks global and per-hospital metrics:
- Global Dice Score & per-region (NCR, ED, ET)
- Hausdorff Distance (HD95)
- CSV summary export
- Convergence curves with moving average smoothing
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np


class FederatedMetricsTracker:
    """
    Accumulates round-by-round federated training metrics, generates CSV reports,
    and plots convergence curves.
    """

    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.history: List[Dict[str, Union[int, float, None]]] = []

    def update(
        self,
        round_id: int,
        global_dice: float,
        dice_ncr: Optional[float] = None,
        dice_ed: Optional[float] = None,
        dice_et: Optional[float] = None,
        hd95: Optional[float] = None,
        loss: Optional[float] = None,
        hospital_dice: Optional[Dict[int, float]] = None,
    ):
        entry = {
            "round": round_id,
            "global_dice": round(global_dice, 4),
            "dice_ncr": round(dice_ncr, 4) if dice_ncr is not None else None,
            "dice_ed": round(dice_ed, 4) if dice_ed is not None else None,
            "dice_et": round(dice_et, 4) if dice_et is not None else None,
            "hd95": round(hd95, 2) if hd95 is not None and not np.isnan(hd95) else None,
            "loss": round(loss, 4) if loss is not None else None,
        }
        if hospital_dice:
            for hid, score in hospital_dice.items():
                entry[f"hospital_{hid}_dice"] = round(score, 4)

        self.history.append(entry)

    def export_csv(self, filename: str = "federated_metrics.csv") -> Path:
        out_path = self.output_dir / filename
        if not self.history:
            return out_path

        fieldnames = list(self.history[0].keys())
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.history:
                clean_row = {k: ("" if v is None else v) for k, v in row.items()}
                writer.writerow(clean_row)
        return out_path

    def export_json(self, filename: str = "federated_metrics.json") -> Path:
        out_path = self.output_dir / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)
        return out_path

    def summary(self) -> Dict[str, Union[int, float]]:
        if not self.history:
            return {}
        best_round = max(self.history, key=lambda r: r.get("global_dice", 0))
        return {
            "total_rounds": len(self.history),
            "best_round": best_round["round"],
            "best_global_dice": best_round["global_dice"],
            "final_global_dice": self.history[-1]["global_dice"],
        }
