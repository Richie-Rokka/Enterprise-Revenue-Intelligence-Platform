"""
Enterprise Revenue Intelligence Platform (ERIP)

Observability Package

Provides enterprise-grade observability capabilities
for the platform, including:

- Centralized logging
- Execution timing
- Memory monitoring
- Pipeline execution summaries

This package serves as the single public interface
for all observability components.
"""

from .logger import get_logger
from .timer import Timer
from .memory import (
    MemoryUsage,
    get_memory_usage,
)
from .summary import PipelineSummary

__version__ = "2.0.0"

__all__ = [
    "get_logger",
    "Timer",
    "MemoryUsage",
    "get_memory_usage",
    "PipelineSummary",
]