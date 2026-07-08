"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : manager.py
Package     : src.runtime
Purpose     : Enterprise Runtime Manager
Author      : ERIP
Version     : 4.0.0

Description
-----------
Public façade for the Enterprise Runtime Kernel.

The Runtime Manager owns the execution lifecycle for platform operations
and provides a unified runtime interface for all ERIP frameworks.

Responsibilities
----------------
- Start execution
- Complete execution
- Fail execution
- Manage framework state
- Expose execution context
- Reset runtime
- Report framework version

===============================================================================
"""

from __future__ import annotations

from src.observability import get_logger

from .context import RuntimeContext
from .lifecycle import RuntimeLifecycle
from .models import (
    ExecutionContext,
    FrameworkState,
)

logger = get_logger(__name__)


# =============================================================================
# Runtime Manager
# =============================================================================


class RuntimeManager:
    """
    Enterprise Runtime Manager.

    Public façade for the Enterprise Runtime Kernel.
    """

    VERSION = "4.0.0"

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *,
        lifecycle: RuntimeLifecycle,
    ) -> None:
        """
        Construct the Enterprise Runtime Manager.

        Parameters
        ----------
        lifecycle
            Shared Runtime Lifecycle.
        """

        self.lifecycle = lifecycle

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    def begin(
        self,
        *,
        framework: str,
        operation: str,
    ) -> ExecutionContext:
        """
        Begin a new framework execution.
        """

        logger.info(
            "Starting %s (%s)",
            framework,
            operation,
        )

        return self.lifecycle.begin(

            framework=framework,

            operation=operation,

        )

    # -------------------------------------------------------------------------

    def state(
        self,
        state: FrameworkState,
    ) -> None:
        """
        Update framework lifecycle state.
        """

        self.lifecycle.state(state)

    # -------------------------------------------------------------------------

    def success(self) -> ExecutionContext:
        """
        Mark execution successful.
        """

        logger.info("Execution completed successfully.")

        return self.lifecycle.success()

    # -------------------------------------------------------------------------

    def failure(
        self,
        error: Exception | str,
    ) -> ExecutionContext:
        """
        Mark execution failed.
        """

        logger.exception(error)

        return self.lifecycle.failure(error)


    # -------------------------------------------------------------------------
    # Runtime Metrics
    # -------------------------------------------------------------------------

    def add_rows_processed(
        self,
        rows: int,
    ) -> None:
        """
        Add processed rows to the current execution.

        Parameters
        ----------
        rows
            Number of rows processed.
        """

        self.lifecycle.add_rows_processed(rows)

    def add_metadata(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Add execution metadata.
        """

        self.lifecycle.add_metadata(key, value)


    # -------------------------------------------------------------------------

    def set_memory_usage(
        self,
        memory_mb: float,
    ) -> None:
        """
        Record memory usage.
        """

        self.lifecycle.set_memory_usage(memory_mb)


    # -------------------------------------------------------------------------

    def set_cpu_usage(
        self,
        cpu_percent: float,
    ) -> None:
        """
        Record CPU utilization.
        """

        self.lifecycle.set_cpu_usage(cpu_percent)

    # -------------------------------------------------------------------------
    # Runtime
    # -------------------------------------------------------------------------

    @property
    def execution(self) -> ExecutionContext | None:
        """
        Current execution context.
        """

        return self.lifecycle.execution

    # -------------------------------------------------------------------------

    def reset(self) -> None:
        """
        Reset runtime lifecycle.
        """

        self.lifecycle = RuntimeLifecycle()

    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return runtime status.
        """

        execution = self.execution

        if execution is None:

            return "IDLE"

        return execution.status.value

    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Return Runtime Framework version.
        """

        return self.VERSION