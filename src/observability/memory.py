"""
Enterprise Revenue Intelligence Platform (ERIP)

Memory Monitoring

Provides standardized process memory monitoring for
ETL pipelines and application diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass

import os

import psutil


@dataclass(slots=True)
class MemoryUsage:
    """
    Memory usage statistics for the current process.
    """

    current_bytes: int
    current_mb: float
    current_gb: float


def get_memory_usage() -> MemoryUsage:
    """
    Return memory usage for the current Python process.

    Returns
    -------
    MemoryUsage
        Current process memory statistics.
    """

    process = psutil.Process(os.getpid())

    memory_bytes = process.memory_info().rss

    memory_mb = memory_bytes / (1024 ** 2)

    memory_gb = memory_bytes / (1024 ** 3)

    return MemoryUsage(
        current_bytes=memory_bytes,
        current_mb=round(memory_mb, 2),
        current_gb=round(memory_gb, 4),
    )