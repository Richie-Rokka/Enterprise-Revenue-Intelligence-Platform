"""
memory.py
Enterprise Revenue Intelligence Platform

Memory monitoring utilities.
"""

import os
import psutil


def get_memory_usage() -> float:
    """
    Returns the current Python process
    memory usage in MB.
    """

    process = psutil.Process(
        os.getpid()
    )

    memory_mb = (
        process.memory_info().rss
        / 1024
        / 1024
    )

    return memory_mb