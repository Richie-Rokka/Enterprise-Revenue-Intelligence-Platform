"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : lifecycle.py
Package     : src.runtime
Purpose     : Enterprise Runtime Lifecycle
Author      : ERIP
Version     : 4.0.0

Description
-----------
Central runtime lifecycle manager for ERIP.

The RuntimeLifecycle owns the execution context for a platform run and
coordinates state transitions across all framework managers.

Responsibilities
----------------
- Create execution contexts
- Manage lifecycle transitions
- Track framework execution
- Record runtime metrics
- Capture execution failures

===============================================================================
"""

from __future__ import annotations

from .context import RuntimeContext
from .models import (
    ExecutionContext,
    FrameworkState,
)


# =============================================================================
# Runtime Lifecycle
# =============================================================================


class RuntimeLifecycle:
    """
    Enterprise Runtime Lifecycle.

    Coordinates execution for the entire platform.
    """

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self._runtime: RuntimeContext | None = None

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    def begin(
        self,
        *,
        framework: str,
        operation: str,
    ) -> ExecutionContext:
        """
        Begin a new execution.
        """

        self._runtime = RuntimeContext(

            framework=framework,

            operation=operation,

        )

        self._runtime.start()

        return self._runtime.execution

    # -------------------------------------------------------------------------

    def state(
        self,
        state: FrameworkState,
    ) -> None:
        """
        Update framework lifecycle state.
        """

        if self._runtime is None:
            return

        self._runtime.set_state(state)

    # -------------------------------------------------------------------------

    def success(self) -> ExecutionContext:
        """
        Complete execution successfully.
        """

        if self._runtime is None:

            raise RuntimeError(
                "Runtime has not been started."
            )

        self._runtime.succeed()

        return self._runtime.execution

    # -------------------------------------------------------------------------

    def failure(
        self,
        error: Exception | str,
    ) -> ExecutionContext:
        """
        Complete execution with failure.
        """

        if self._runtime is None:

            raise RuntimeError(
                "Runtime has not been started."
            )

        self._runtime.fail(error)

        return self._runtime.execution


    # -------------------------------------------------------------------------
    # Runtime Metrics
    # -------------------------------------------------------------------------

    def add_rows_processed(
        self,
        rows: int,
    ) -> None:
        """
        Add processed rows.
        """

        if self._runtime is None:
            return

        self._runtime.add_rows_processed(rows)


    # -------------------------------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Add execution metadata.
        """

        if self._runtime is None:
            return

        self._runtime.add_metadata(key, value)


    # -------------------------------------------------------------------------

    def set_memory_usage(
        self,
        memory_mb: float,
    ) -> None:
        """
        Record memory usage.
        """

        if self._runtime is None:
            return

        self._runtime.set_memory_usage(memory_mb)


    # -------------------------------------------------------------------------

    def set_cpu_usage(
        self,
        cpu_percent: float,
    ) -> None:
        """
        Record CPU utilization.
        """

        if self._runtime is None:
            return

        self._runtime.set_cpu_usage(cpu_percent)

    # -------------------------------------------------------------------------

    @property
    def execution(self) -> ExecutionContext | None:
        """
        Current execution context.
        """

        if self._runtime is None:
            return None

        return self._runtime.execution