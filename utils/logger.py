"""
Member 5 - Integration & QA
Task: Logging utility shared across all modules
Day 1-2: Centralized logging setup
"""

import logging
import os
from datetime import datetime


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a configured logger that writes to both console and file.

    Args:
        name: Logger name (e.g., 'FedMedServer', 'HospitalNode-1')
        level: Logging level (default: INFO)

    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(level)

    # Format: [2026-08-30 17:00:00] [FedMedServer] INFO: message
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler — one log file per day
    log_filename = os.path.join(
        LOG_DIR,
        f"fedmed_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
