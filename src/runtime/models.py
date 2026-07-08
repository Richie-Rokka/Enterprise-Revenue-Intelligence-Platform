"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : models.py
Package     : src.runtime
Purpose     : Enterprise Runtime Models
Author      : ERIP
Version     : 4.0.0

Description
-----------
Shared runtime models used across the Enterprise Runtime Kernel.

These models provide a common execution lifecycle for every framework
within ERIP.

Responsibilities
----------------
- Framework lifecycle states
- Execution status
- Runtime metrics
- Execution context

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


# =============================================================================
# Framework Lifecycle
# =============================================================================


class FrameworkState(str, Enum):
    """
    Runtime lifecycle state of a framework.
    """

    INITIALIZED = "INITIALIZED"

    DEPLOYING = "DEPLOYING"

    LOADING = "LOADING"

    VALIDATING = "VALIDATING"

    REFRESHING = "REFRESHING"

    READY = "READY"

    FAILED = "FAILED"


# =============================================================================
# Execution Status
# =============================================================================


class ExecutionStatus(str, Enum):
    """
    Execution outcome.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"


# =============================================================================
# Runtime Metrics
# =============================================================================


@dataclass(slots=True)
class RuntimeMetrics:
    """
    Runtime performance metrics.
    """

    execution_time_seconds: float = 0.0

    rows_processed: int = 0

    cpu_usage_percent: float | None = None

    memory_usage_mb: float | None = None


# =============================================================================
# Execution Context
# =============================================================================


@dataclass(slots=True)
class ExecutionContext:
    """
    Shared execution context.

    A single instance of this object is intended to flow through the
    entire platform execution pipeline.
    """

    execution_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    framework: str = ""

    operation: str = ""

    state: FrameworkState = FrameworkState.INITIALIZED

    status: ExecutionStatus = ExecutionStatus.PENDING

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    completed_at: datetime | None = None

    metrics: RuntimeMetrics = field(
        default_factory=RuntimeMetrics
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    error: str | None = None