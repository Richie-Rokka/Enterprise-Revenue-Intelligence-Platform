"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : context.py
Package     : src.runtime
Purpose     : Enterprise Runtime Context
Author      : ERIP
Version     : 4.0.0

Description
-----------
Runtime execution context shared across the Enterprise Revenue
Intelligence Platform.

The RuntimeContext owns the lifecycle of a platform execution and is
shared across Warehouse, Semantic, Monitoring, Quality and future
frameworks.

Responsibilities
----------------
- Manage execution lifecycle
- Track runtime state
- Record execution timestamps
- Capture failures
- Collect runtime metrics

===============================================================================
"""

from __future__ import annotations

from datetime import datetime

from .models import (
    ExecutionContext,
    ExecutionStatus,
    FrameworkState,
)


# =============================================================================
# Runtime Context
# =============================================================================


class RuntimeContext:
    """
    Enterprise Runtime Context.

    Owns the execution lifecycle for a platform operation.
    """

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *,
        framework: str,
        operation: str,
    ) -> None:

        self._context = ExecutionContext(

            framework=framework,

            operation=operation,

        )

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def execution(self) -> ExecutionContext:
        """
        Return the execution context.
        """

        return self._context

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    def start(self) -> None:
        """
        Start execution.
        """

        self._context.status = ExecutionStatus.RUNNING

        self._context.started_at = datetime.utcnow()

    # -------------------------------------------------------------------------

    def set_state(
        self,
        state: FrameworkState,
    ) -> None:
        """
        Update framework lifecycle state.
        """

        self._context.state = state

    # -------------------------------------------------------------------------

    def succeed(self) -> None:
        """
        Mark execution as successful.
        """

        self._context.status = ExecutionStatus.SUCCESS

        self._context.state = FrameworkState.READY

        self._context.completed_at = datetime.utcnow()

        self._update_elapsed_time()

    # -------------------------------------------------------------------------

    def fail(
        self,
        error: Exception | str,
    ) -> None:
        """
        Mark execution as failed.
        """

        self._context.status = ExecutionStatus.FAILED

        self._context.state = FrameworkState.FAILED

        self._context.completed_at = datetime.utcnow()

        self._context.error = self._normalize_error(error)

        self._update_elapsed_time()

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

        self._context.metrics.rows_processed += rows

    # -------------------------------------------------------------------------

    def set_memory_usage(
        self,
        memory_mb: float,
    ) -> None:
        """
        Record memory usage.
        """

        self._context.metrics.memory_usage_mb = memory_mb

    # -------------------------------------------------------------------------

    def set_cpu_usage(
        self,
        cpu_percent: float,
    ) -> None:
        """
        Record CPU utilization.
        """

        self._context.metrics.cpu_usage_percent = cpu_percent

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Add execution metadata.
        """

        self._context.metadata[key] = value

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _update_elapsed_time(self) -> None:
        """
        Calculate execution duration.
        """

        if self._context.completed_at is None:
            return

        self._context.metrics.execution_time_seconds = (

            self._context.completed_at

            - self._context.started_at

        ).total_seconds()

    # -------------------------------------------------------------------------

    def _normalize_error(
        self,
        error: Exception | str,
    ) -> str:
        """
        Convert an exception into a concise runtime message.

        Runtime history should contain a short diagnostic while
        detailed SQL and stack traces remain in the application log.
        """

        message = str(error)

        #
        # Remove embedded SQL statements.
        #

        if "[SQL:" in message:

            message = message.split("[SQL:", 1)[0].strip()

        #
        # Remove SQLAlchemy documentation links.
        #

        if "(Background on this error" in message:

            message = message.split(
                "(Background on this error",
                1,
            )[0].strip()

        #
        # Collapse whitespace.
        #

        message = " ".join(message.split())

        return message