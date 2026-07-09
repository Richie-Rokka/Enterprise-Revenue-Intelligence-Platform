"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : monitoring_stage.py
Package     : src.orchestration.stages
Purpose     : Monitoring Pipeline Stage
Author      : ERIP
Version     : 4.0.0

Description
-----------
Pipeline adapter for the Enterprise Monitoring Framework.

This stage allows the Enterprise Pipeline Engine to execute the Monitoring
Framework without coupling orchestration to MonitoringManager.

Responsibilities
----------------
- Execute MonitoringManager
- Convert ExecutionResult into StageResult
- Publish execution metadata
- Return standardized StageResult

===============================================================================
"""

from __future__ import annotations

from src.monitoring.manager import MonitoringManager

from src.orchestration.execution_context import ExecutionContext
from src.orchestration.stage import Stage
from src.orchestration.stage_result import (
    StageResult,
    StageStatus,
)


class MonitoringStage(Stage):
    """
    Pipeline adapter for the Enterprise Monitoring Framework.
    """

    name = "monitoring"

    description = "Execute Enterprise Monitoring Framework"

    # =========================================================================
    # Construction
    # =========================================================================

    

    # =========================================================================
    # Lifecycle
    # =========================================================================

    def validate(
        self,
        context: ExecutionContext,
    ) -> bool:
        """
        Validate Monitoring stage prerequisites.
        """

        return True

    # -------------------------------------------------------------------------

    def execute(
        self,
        context: ExecutionContext,
    ) -> StageResult:
        """
        Execute the Monitoring Framework.
        """

        context.set_stage(self.name)

        manager = context.services.monitoring_manager

        execution = manager.statistics()

        status = (
            StageStatus.SUCCESS
            if execution.success
            else StageStatus.FAILED
        )

        result = StageResult(

            stage_name=self.name,

            status=status,

            rows_processed=execution.rows_processed,

            rows_loaded=execution.rows_processed,

            warnings=0,

            errors=0 if execution.success else 1,

            message=(
                "Monitoring statistics completed successfully."
                if execution.success
                else "Monitoring statistics failed."
            ),
        )

        result.add_metadata(
            "framework_status",
            manager.status(),
        )

        result.add_metadata(
            "operation",
            "statistics",
        )

        result.add_metadata(
            "script_name",
            execution.script_name,
        )

        result.add_metadata(
            "execution_time_seconds",
            execution.execution_time_seconds,
        )

        return result

    # -------------------------------------------------------------------------

    def before_execute(
        self,
        context: ExecutionContext,
    ) -> None:

        context.logger.info(
            "Starting Monitoring Stage..."
        )

    # -------------------------------------------------------------------------

    def after_execute(
        self,
        context: ExecutionContext,
        result: StageResult,
    ) -> None:

        context.logger.info(
            "Monitoring Stage Completed."
        )

    # -------------------------------------------------------------------------

    def cleanup(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Cleanup stage resources.
        """

        pass