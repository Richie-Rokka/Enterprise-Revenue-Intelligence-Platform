"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : runtime_presenter.py
Package     : src.presentation
Purpose     : Enterprise Runtime Presenter
Author      : ERIP
Version     : 4.0.0

Description
-----------
Presentation layer for the Enterprise Runtime Framework.

Transforms Runtime execution models into professional operational
reports using the Enterprise Report Builder.

Responsibilities
----------------
- Runtime execution presentation
- Runtime status presentation
- Runtime metrics presentation
- Runtime error presentation

===============================================================================
"""

from __future__ import annotations

from src.runtime.models import ExecutionContext

from .base_presenter import BasePresenter
from .console import Console
from .formatter import Formatter
from .report import Report


# =============================================================================
# Runtime Presenter
# =============================================================================


class RuntimePresenter(BasePresenter):
    """
    Enterprise Runtime Presenter.
    """

    # -------------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        context: ExecutionContext | None,
    ) -> str:
        """
        Build the Runtime execution report.
        """

        if context is None:

            return (
                Report("Runtime Execution Summary")
                .add_section(
                    title="Status",
                    body=Console.info(
                        "No active runtime execution."
                    ),
                )
                .build()
            )

        return (
            Report("Runtime Execution Summary")

            .add_section(
                title="Execution",
                body=cls._execution(context),
            )

            .add_section(
                title="Status",
                body=cls._status(context),
            )

            .add_section(
                title="Timing",
                body=cls._timing(context),
            )

            .add_section(
                title="Metrics",
                body=cls._metrics(context),
            )

            .add_section(
                title="Metadata",
                body=cls._metadata(context),
            )

            .add_section(
                title="Error",
                body=cls._error(context),
            )

            .build()
        )

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    @staticmethod
    def _execution(
        context: ExecutionContext,
    ) -> str:
        """
        Build execution section.
        """

        return Console.join(

            Console.key_value(
                "Execution ID",
                context.execution_id,
            ),

            Console.key_value(
                "Framework",
                context.framework,
            ),

            Console.key_value(
                "Operation",
                context.operation,
            ),

        )

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    @staticmethod
    def _status(
        context: ExecutionContext,
    ) -> str:
        """
        Build status section.
        """

        return Console.join(

            Console.key_value(
                "Status",
                context.status.value,
            ),

            Console.key_value(
                "State",
                context.state.value,
            ),

        )

    # -------------------------------------------------------------------------
    # Timing
    # -------------------------------------------------------------------------

    @staticmethod
    def _timing(
        context: ExecutionContext,
    ) -> str:
        """
        Build timing section.
        """

        return Console.join(

            Console.key_value(
                "Started",
                Formatter.datetime(
                    context.started_at,
                ),
            ),

            Console.key_value(
                "Completed",
                Formatter.datetime(
                    context.completed_at,
                ),
            ),

            Console.key_value(
                "Elapsed",
                Formatter.duration(
                    context.metrics.execution_time_seconds,
                ),
            ),

        )

    # -------------------------------------------------------------------------
    # Metrics
    # -------------------------------------------------------------------------

    @staticmethod
    def _metrics(
        context: ExecutionContext,
    ) -> str:
        """
        Build runtime metrics section.
        """

        return Console.join(

            Console.key_value(
                "Rows Processed",
                Formatter.rows(
                    context.metrics.rows_processed,
                ),
            ),

            Console.key_value(
                "Memory Usage",
                Formatter.memory(
                    context.metrics.memory_usage_mb,
                ),
            ),

            Console.key_value(
                "CPU Usage",
                Formatter.percent(
                    context.metrics.cpu_usage_percent,
                ),
            ),

        )

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    @classmethod
    def _metadata(
        cls,
        context: ExecutionContext,
    ) -> str:
        """
        Build metadata section.
        """

        return cls.metadata(
            context.metadata,
        )

    # -------------------------------------------------------------------------
    # Error
    # -------------------------------------------------------------------------

    @staticmethod
    def _error(
        context: ExecutionContext,
    ) -> str:
        """
        Build error section.
        """

        return Console.key_value(

            "Message",

            Formatter.text(
                context.error,
            ),

        )