"""Application event logging."""

import logging as standard_logging
from pathlib import Path


LOG_FILE = Path("digital_twin_events.log")


def get_logger(name: str = "digital_twin") -> standard_logging.Logger:
    """Create and configure the Digital Twin event logger."""

    logger = standard_logging.getLogger(name)

    if not logger.handlers:
        formatter = standard_logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        console_handler = standard_logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = standard_logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    logger.setLevel(standard_logging.INFO)

    return logger