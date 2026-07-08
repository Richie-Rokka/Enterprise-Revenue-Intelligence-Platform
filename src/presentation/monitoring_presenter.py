"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : monitoring_presenter.py
Package     : src.presentation
Purpose     : Enterprise Monitoring Presenter

Author      : ERIP
Version     : 3.0.0

Description
-----------
Enterprise presenter for the Monitoring Framework.

Renders Monitoring Framework models using the Enterprise Presentation
Framework.

===============================================================================
"""

from __future__ import annotations

from src.database.database_executor import ExecutionResult

from src.presentation.base_presenter import BasePresenter
from src.presentation.console import Console
from src.presentation.formatter import Formatter
from src.presentation.report import Report

from src.monitoring.models import (
    MonitoringDashboard,
    MonitoringValidationResult,
    PlatformHealth,
    RuntimeStatistics,
)


# =============================================================================
# Monitoring Presenter
# =============================================================================


class MonitoringPresenter(BasePresenter):
    """
    Enterprise Monitoring Presenter.
    """

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        model: object,
    ) -> str:
        """
        Render a Monitoring presentation model.
        """

        if isinstance(
            model,
            PlatformHealth,
        ):

            return cls._health(
                model
            )

        if isinstance(
            model,
            RuntimeStatistics,
        ):

            return cls._metrics(
                model
            )

        if isinstance(
            model,
            MonitoringDashboard,
        ):

            return cls._dashboard(
                model
            )

        if isinstance(
            model,
            MonitoringValidationResult,
        ):

            return cls._validation(
                model
            )

        if isinstance(
            model,
            ExecutionResult,
        ):

            return cls._operation(
                model
            )

        raise TypeError(

            f"Unsupported Monitoring presentation model: "

            f"{type(model).__name__}"

        )

    # -------------------------------------------------------------------------
    # Platform Health
    # -------------------------------------------------------------------------

    @classmethod
    def _health(
        cls,
        result: PlatformHealth,
    ) -> str:
        """
        Render Enterprise Platform Health.
        """

        report = Report(

            "Platform Health Summary"

        )

        report.add_section(

            title="Platform",

            body=Console.key_values(

                database=result.database,

                warehouse=result.warehouse,

                semantic=result.semantic,

                overall=result.overall,

            ),

        )

        return report.build()

    # -------------------------------------------------------------------------
    # Runtime Metrics
    # -------------------------------------------------------------------------

    @classmethod
    def _metrics(
        cls,
        result: RuntimeStatistics,
    ) -> str:
        """
        Render Runtime metrics.
        """

        report = Report(

            "Runtime Metrics Summary"

        )

        report.add_section(

            title="Runtime",

            body=Console.key_values(

                execution_time=Formatter.duration(

                    result.execution_time_seconds

                ),

                memory_usage=f"{result.memory_usage_mb:.2f} MB",

            ),

        )

        return report.build()

    # -------------------------------------------------------------------------
    # Enterprise Dashboard
    # -------------------------------------------------------------------------

    @classmethod
    def _dashboard(
        cls,
        result: MonitoringDashboard,
    ) -> str:
        """
        Render Enterprise Monitoring Dashboard.
        """

        report = Report(

            "Enterprise Monitoring Dashboard"

        )

        report.add_section(

            title="Platform Health",

            body=Console.key_values(

                database=result.platform_health.database,

                warehouse=result.platform_health.warehouse,

                semantic=result.platform_health.semantic,

                overall=result.platform_health.overall,

            ),

        )

        report.add_section(

            title="Runtime",

            body=Console.key_values(

                execution_time=Formatter.duration(

                    result.runtime.execution_time_seconds

                ),

                memory_usage=f"{result.runtime.memory_usage_mb:.2f} MB",

            ),

        )

        report.add_section(

            title="Warehouse",

            body=Console.key_values(

                dimensions_loaded=result.warehouse.dimensions_loaded,

                fact_tables_loaded=result.warehouse.fact_tables_loaded,

                rows_processed=f"{result.warehouse.rows_processed:,}",

            ),

        )

        report.add_section(

            title="Semantic",

            body=Console.key_values(

                views_deployed=result.semantic.views_deployed,

                validation_checks=result.semantic.validation_checks,

                deployment_success=Formatter.boolean(

                    result.semantic.deployment_success

                ),

            ),

        )

        report.add_section(

            title="Deployment",

            body=Console.key_values(

                deployment_success=Formatter.boolean(

                    result.deployment.deployment_success

                ),

                scripts_executed=result.deployment.scripts_executed,

                execution_time=Formatter.duration(

                    result.deployment.execution_time_seconds

                ),

            ),

        )

        return report.build()

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    @classmethod
    def _validation(
        cls,
        result: MonitoringValidationResult,
    ) -> str:
        """
        Render Monitoring validation summary.
        """

        report = Report(

            "Monitoring Validation Summary"

        )

        report.add_section(

            title="Validation",

            body=Console.key_values(

                status=(

                    "PASSED"

                    if result.passed

                    else "FAILED"

                ),

                checks_performed=result.checks_performed,

                failures=len(

                    result.failures

                ),

            ),

        )

        if result.failures:

            report.add_section(

                title="Validation Failures",

                body=Console.join(

                    *result.failures

                ),

            )

        return report.build()

    # -------------------------------------------------------------------------
    # Operation
    # -------------------------------------------------------------------------

    @classmethod
    def _operation(
        cls,
        result: ExecutionResult,
    ) -> str:
        """
        Render Monitoring operation summary.
        """

        report = Report(

            "Monitoring Operation Summary"

        )

        report.add_section(

            title="Execution",

            body=Console.key_values(

                script_name=result.script_name,

                success=Formatter.boolean(

                    result.success

                ),

                execution_time=Formatter.duration(

                    result.execution_time_seconds

                ),

            ),

        )

        if result.error:

            report.add_section(

                title="Error",

                body=Formatter.text(

                    result.error

                ),

            )

        return report.build()