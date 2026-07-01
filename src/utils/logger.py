"""
logger.py
Enterprise Revenue Intelligence Platform

Central logging configuration and helper functions.
"""

import logging
from pathlib import Path
from datetime import datetime


# =====================================================
# Logger Configuration
# =====================================================

def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    Creates:

    • Console logger

    • Timestamped log file
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = log_directory / f"{timestamp}.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# =====================================================
# Section Logging
# =====================================================

def log_section(logger, title):
    """
    Print a section header.
    """

    logger.info("")
    logger.info("=" * 70)
    logger.info(title)
    logger.info("=" * 70)


# =====================================================
# Pipeline Stage
# =====================================================

def log_stage(logger, step, total_steps, message):
    """
    Log pipeline progress.

    Example:

    [2/5] Building Fact Table
    """

    logger.info("")
    logger.info(
        f"[{step}/{total_steps}] {message}"
    )


# =====================================================
# Success
# =====================================================

def log_success(logger, message):
    """
    Log successful completion.
    """

    logger.info(f"[OK] {message}")


# =====================================================
# Warning
# =====================================================

def log_warning(logger, message):
    """
    Log warning message.
    """

    logger.warning(f"[WARNING] {message}")


# =====================================================
# Error
# =====================================================

def log_error(logger, message):
    """
    Log error message.
    """

    logger.error(f"[ERROR] {message}")


# =====================================================
# Pipeline Summary
# =====================================================

def log_summary(logger, summary):
    """
    Print execution summary.
    """

    logger.info("")
    logger.info("Summary")
    logger.info("-" * 40)

    for key, value in summary.items():

        label = key.replace("_", " ").title()

        if isinstance(value, int):

            logger.info(
                f"{label:<15}: {value:,}"
            )

        else:

            logger.info(
                f"{label:<15}: {value}"
            )

def log_pipeline_summary(
    logger,
    summaries,
    execution_time=None,
    memory_usage=None
):
    """
    Log the complete pipeline execution summary.
    """

    logger.info("")
    logger.info("=" * 65)
    logger.info("PIPELINE SUMMARY")
    logger.info("=" * 65)
    logger.info("")

    logger.info(
        f"{'Table':<30}{'Rows Loaded':>15}"
    )

    logger.info("-" * 45)

    total_tables = 0

    for summary in summaries:

        logger.info(
            f"{summary['table']:<30}"
            f"{summary['rows_loaded']:>15,}"
        )

        total_tables += 1

    logger.info("-" * 45)

    logger.info(
        f"{'Total Tables Loaded':<30}"
        f"{total_tables:>15}"
    )

    if execution_time is not None:

        logger.info(
            f"{'Execution Time (sec)':<30}"
            f"{execution_time:>15.2f}"
        )

    if memory_usage is not None:

        logger.info(
            f"{'Memory Usage (MB)':<30}"
            f"{memory_usage:>15.2f}"
        )

    logger.info("=" * 65)