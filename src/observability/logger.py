"""
Enterprise Revenue Intelligence Platform (ERIP)

Enterprise Logger

Creates standardized loggers for the platform.
"""

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

from src.config.config import config
from src.observability.formatter import EnterpriseFormatter


_LOGGERS = {}


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured enterprise logger.

    Parameters
    ----------
    name : str
        Logger name.

    Returns
    -------
    logging.Logger
    """

    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)

    logger.setLevel(
        getattr(
            logging,
            config.logging.level.upper()
        )
    )

    logger.propagate = False

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = EnterpriseFormatter()

    # -----------------------------------------
    # Create Logs Directory
    # -----------------------------------------

    log_directory = Path(
        config.logging.log_directory
    )

    log_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    log_file = (
        log_directory
        / config.logging.log_filename
    )

    # -----------------------------------------
    # Console Handler
    # -----------------------------------------

    if config.logging.console_logging:

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            console_handler
        )

    # -----------------------------------------
    # Rotating File Handler
    # -----------------------------------------

    if config.logging.file_logging:

        file_handler = RotatingFileHandler(

            filename=log_file,

            maxBytes=(
                config.logging.rotation.max_file_size_mb
                * 1024
                * 1024
            ),

            backupCount=(
                config.logging.rotation.backup_count
            ),

            encoding="utf-8",
        )

        file_handler.setFormatter(
            formatter
        )

        logger.addHandler(
            file_handler
        )

    _LOGGERS[name] = logger

    return logger