"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : pipeline.py
Package     : src.orchestration
Purpose     : Enterprise Pipeline Engine
Author      : ERIP
Version     : 2.1.0

Description
-----------
Coordinates execution of all registered pipeline stages.

Responsibilities
----------------
- Execute configured stages
- Maintain execution order
- Collect stage results
- Handle stage failures
- Return pipeline results

===============================================================================
"""

from __future__ import annotations

from src.orchestration.execution_context import ExecutionContext
from src.orchestration.stage_registry import StageRegistry
from src.orchestration.stage_result import (
    StageResult,
    StageStatus,
)


class Pipeline:
    """
    Enterprise Pipeline Engine.
    """

    def __init__(
        self,
        context: ExecutionContext,
    ) -> None:

        self.context = context

        self.logger = context.logger

        self.results: list[StageResult] = []

    # -------------------------------------------------------------------------

    def run(self) -> list[StageResult]:
        """
        Execute the configured pipeline.
        """

        stages = self.context.config.pipeline.stages

        total_stages = len(stages)

        self.logger.info("-" * 70)
        self.logger.info("Pipeline Execution Started")
        self.logger.info("-" * 70)

        for index, stage_name in enumerate(stages, start=1):

            self.logger.info(
                "[%s/%s] %s",
                index,
                total_stages,
                stage_name,
            )

            stage = StageRegistry.get(stage_name)

            stage.before_execute(self.context)

            # -------------------------------------------------------------
            # Validate Stage
            # -------------------------------------------------------------

            if not stage.validate(self.context):

                result = StageResult(
                    stage_name=stage.name,
                    status=StageStatus.SKIPPED,
                    message="Stage validation failed.",
                )

                result.complete()

                self.results.append(result)

                self.logger.warning(
                    "Stage skipped: %s",
                    stage.name,
                )

                continue

            # -------------------------------------------------------------
            # Execute Stage
            # -------------------------------------------------------------

            try:

                result = stage.execute(self.context)

                result.complete()

                stage.after_execute(
                    self.context,
                    result,
                )

                self.results.append(result)

                self.logger.info(
                    "Stage completed successfully."
                )

            except Exception as error:

                result = StageResult(
                    stage_name=stage.name,
                    status=StageStatus.FAILED,
                    message=str(error),
                )

                result.complete()

                self.results.append(result)

                self.logger.exception(
                    "Stage failed: %s",
                    stage.name,
                )

                raise

            finally:

                stage.cleanup(self.context)

        self.logger.info("-" * 70)
        self.logger.info("Pipeline Execution Finished")
        self.logger.info("-" * 70)

        return self.results

    # -------------------------------------------------------------------------

    @property
    def succeeded(self) -> bool:
        """
        Return True if all executed stages succeeded.
        """

        return all(
            result.status == StageStatus.SUCCESS
            for result in self.results
        )

    @property
    def failed(self) -> bool:
        """
        Return True if any stage failed.
        """

        return any(
            result.status == StageStatus.FAILED
            for result in self.results
        )

    @property
    def total_rows_processed(self) -> int:
        """
        Total processed rows.
        """

        return sum(
            result.rows_processed
            for result in self.results
        )

    @property
    def total_rows_loaded(self) -> int:
        """
        Total loaded rows.
        """

        return sum(
            result.rows_loaded
            for result in self.results
        )