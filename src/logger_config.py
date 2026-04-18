import logging
from pathlib import Path


def setup_logger(log_file_path: Path) -> logging.Logger:
    """
    Configure and return a logger that writes to both console and file.

    Args:
        log_file_path (Path): Path to the log file.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("financial_pipeline")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if the script is run multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger