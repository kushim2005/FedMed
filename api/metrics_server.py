#!/usr/bin/env python3
"""
api/metrics_server.py
FedMed — FastAPI Metrics Server for React Dashboard.

Author: Vasu Sree (DevOps)
Week 4: Dashboard API backend

Serves real-time FL training metrics, hospital status, and privacy
budget data to the React dashboard via REST API.

Endpoints:
    GET /api/metrics    — per-round Dice, Loss, per-class metrics
    GET /api/hospitals  — hospital node status and connection info
    GET /api/privacy    — per-round epsilon, delta, budget used
    GET /api/health     — health check
"""

import json
import os
from pathlib import Path
from typing import List

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

try:
    from flask import Flask, jsonify
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

METRICS_CSV = os.environ.get("METRICS_CSV", "logs/week4/dp_metrics.csv")
PRIVACY_CSV = os.environ.get("PRIVACY_CSV", "logs/week4/privacy_budget.csv")
API_PORT = int(os.environ.get("API_PORT", "8000"))
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")

# Demo data used when CSV files are not yet available
DEMO_METRICS = [
    {
        "round": i + 1,
        "dice": round(0.42 + i * 0.028, 4),
        "loss": round(0.72 - i * 0.055, 4),
        "dice_et": round(0.41 + i * 0.030, 4),
        "dice_ed": round(0.48 + i * 0.027, 4),
        "dice_ncr": round(0.30 + i * 0.027, 4),
        "hd95": round(22.0 - i * 0.78, 2),
        "clients": 3,
        "round_time": round(18.2 + (i % 3) * 0.4, 1),
    }
    for i in range(10)
]

DEMO_HOSPITALS = [
    {
        "id": "aiims_delhi",
        "name": "AIIMS Delhi",
        "location": "New Delhi, India",
        "status": "connected",
        "samples": 187,
        "last_round_dice": 0.681,
        "current_epsilon": 2.79,
        "flag": "🇮🇳",
    },
    {
        "id": "mayo_clinic",
        "name": "Mayo Clinic",
        "location": "Rochester, USA",
        "status": "connected",
        "samples": 224,
        "last_round_dice": 0.689,
        "current_epsilon": 2.79,
        "flag": "🇺🇸",
    },
    {
        "id": "nhs_london",
        "name": "NHS London",
        "location": "London, UK",
        "status": "connected",
        "samples": 163,
        "last_round_dice": 0.678,
        "current_epsilon": 2.79,
        "flag": "🇬🇧",
    },
]

DEMO_PRIVACY = [
    {
        "round": i + 1,
        "epsilon": round((i + 1) * 0.279, 4),
        "delta": 1e-5,
        "noise_multiplier": 1.1,
        "clip_norm": 1.0,
        "budget_pct": round(((i + 1) * 0.279) / 3.5 * 100, 1),
    }
    for i in range(10)
]


def load_metrics_from_csv(path: str) -> List[dict]:
    """Load round metrics from CSV file if available."""
    if not Path(path).exists():
        return DEMO_METRICS

    import csv
    rows = []
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                parsed_row = {
                    k: float(v) if v.replace(".", "").isdigit() else v
                    for k, v in row.items()
                }
                rows.append(parsed_row)
    except Exception:
        return DEMO_METRICS

    return rows if rows else DEMO_METRICS


def load_privacy_from_csv(path: str) -> List[dict]:
    """Load privacy records from CSV file if available."""
    if not Path(path).exists():
        return DEMO_PRIVACY

    import csv
    rows = []
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entry = {k: float(v) if v.replace(".", "").replace("e-", "").isdigit()
                         else v for k, v in row.items()}
                if "epsilon" in entry:
                    entry["budget_pct"] = round(
                        float(entry["epsilon"]) / 3.5 * 100, 1
                    )
                rows.append(entry)
    except Exception:
        return DEMO_PRIVACY

    return rows if rows else DEMO_PRIVACY


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="FedMed Metrics API",
        description="Real-time FL training metrics for the FedMed Dashboard",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    async def health():
        return {"status": "healthy", "service": "fedmed-api", "version": "1.0.0"}

    @app.get("/api/metrics")
    async def get_metrics():
        return load_metrics_from_csv(METRICS_CSV)

    @app.get("/api/hospitals")
    async def get_hospitals():
        return DEMO_HOSPITALS

    @app.get("/api/privacy")
    async def get_privacy():
        return load_privacy_from_csv(PRIVACY_CSV)

    @app.get("/")
    async def root():
        return {
            "name": "FedMed Metrics API",
            "endpoints": ["/api/metrics", "/api/hospitals", "/api/privacy", "/api/health"],
        }

else:
    app = None


def run_flask():
    """Run Flask server when FastAPI is not available."""
    flask_app = Flask("fedmed_metrics")
    CORS(flask_app, origins=CORS_ORIGINS)

    @flask_app.route("/api/health")
    def health():
        return jsonify({"status": "healthy", "service": "fedmed-api", "version": "1.0.0"})

    @flask_app.route("/api/metrics")
    def metrics():
        return jsonify(load_metrics_from_csv(METRICS_CSV))

    @flask_app.route("/api/hospitals")
    def hospitals():
        return jsonify(DEMO_HOSPITALS)

    @flask_app.route("/api/privacy")
    def privacy():
        return jsonify(load_privacy_from_csv(PRIVACY_CSV))

    @flask_app.route("/")
    def root():
        return jsonify({
            "name": "FedMed Metrics API",
            "endpoints": ["/api/metrics", "/api/hospitals", "/api/privacy", "/api/health"],
        })

    print(f"Starting FedMed Metrics API on port {API_PORT}...")
    flask_app.run(host="0.0.0.0", port=API_PORT, debug=False)


if __name__ == "__main__":
    if FASTAPI_AVAILABLE:
        import uvicorn
        print(f"Starting FedMed Metrics API on port {API_PORT}...")
        uvicorn.run("api.metrics_server:app", host="0.0.0.0", port=API_PORT, reload=False)
    elif FLASK_AVAILABLE:
        run_flask()
    else:
        raise ImportError(
            "FastAPI or Flask required: pip install fastapi uvicorn OR pip install flask flask-cors"
        )
