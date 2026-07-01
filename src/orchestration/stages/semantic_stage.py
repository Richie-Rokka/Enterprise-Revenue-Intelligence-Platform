"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : semantic_stage.py
Package     : src.orchestration.stages
Purpose     : Semantic Layer Pipeline Stage
Author      : ERIP
Version     : 2.0.0

Description
-----------
Pipeline stage responsible for deploying and validating the Enterprise
Semantic Layer.

Responsibilities
----------------
- Execute SemanticManager
- Return standardized StageResult
- Report deployment metrics

===============================================================================
"""

from __future__ import annotations

from src.semantic.manager import SemanticManager

from src.orchestration.execution_context import ExecutionContext
from src.orchestration.stage import Stage
from src.orchestration.stage_result import (
    StageResult,
    StageStatus,
)


class SemanticStage(Stage):
    """
    Pipeline stage responsible for semantic layer deployment.
    """

    name = "semantic"

    def __init__(self) -> None:

        self.manager = SemanticManager()

    # -------------------------------------------------------------------------

    def validate(
        self,
        context: ExecutionContext,
    ) -> bool:
        """
        Validate stage prerequisites.
        """

        return True

    # -------------------------------------------------------------------------

    def execute(
        self,
        context: ExecutionContext,
    ) -> StageResult:
        """
        Execute semantic deployment.
        """

        context.set_stage(self.name)

        deployment = self.manager.rebuild()

        status = (
            StageStatus.SUCCESS
            if deployment.success
            else StageStatus.FAILED
        )

        result = StageResult(

            stage_name=self.name,

            status=status,

            rows_processed=deployment.scripts_executed,

            rows_loaded=deployment.scripts_executed,

            warnings=0,

            errors=0 if deployment.success else 1,

            message=(
                "Semantic layer deployed successfully."
                if deployment.success
                else "Semantic layer deployment failed."
            ),
        )

        result.add_metadata(
            "validation_passed",
            deployment.validation_passed,
        )

        result.add_metadata(
            "scripts_executed",
            deployment.scripts_executed,
        )

        return result

    # -------------------------------------------------------------------------

    def before_execute(
        self,
        context: ExecutionContext,
    ) -> None:

        context.logger.info(
            "Starting Semantic Stage..."
        )

    # -------------------------------------------------------------------------

    def after_execute(
        self,
        context: ExecutionContext,
        result: StageResult,
    ) -> None:

        context.logger.info(
            "Semantic Stage Completed."
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