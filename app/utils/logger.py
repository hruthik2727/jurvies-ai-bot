"""
app/utils/logger.py
───────────────────
Structured logging with file + console output using Python's logging module.
"""

import logging
import sys
from pathlib import Path
from app.core.config import settings, BASE_DIR


def setup_logger(name: str = "jurvies") -> logging.Logger:
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    if logger.handlers:
        return logger  # Already configured

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # File handler
    file_handler = logging.FileHandler(log_dir / "jurvies.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
