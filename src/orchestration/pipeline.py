"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : pipeline.py
Package     : src.orchestration
Purpose     : Enterprise Pipeline Engine
Author      : ERIP
Version     : 2.2.0

Description
-----------
Enterprise execution pipeline responsible for coordinating the execution of
all registered platform stages.

Responsibilities
----------------
- Execute configured stages
- Maintain execution order
- Execute stage lifecycle
- Validate stage prerequisites
- Handle execution failures
- Aggregate execution metrics
- Synchronize ExecutionContext
- Return pipeline execution results

Architecture
------------
Platform
    │
    ▼
ExecutionContext
    │
    ▼
Pipeline
    │
    ▼
Stage Registry
    │
    ▼
Stage
    │
    ▼
Managers
    │
    ▼
Runtime

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

    Coordinates execution of all configured platform stages while maintaining
    execution order, lifecycle management, telemetry collection and execution
    statistics.
    """

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(
        self,
        context: ExecutionContext,
    ) -> None:

        self.context = context

        self.logger = context.logger

        self.results: list[StageResult] = []

    # =========================================================================
    # Pipeline Execution
    # =========================================================================

    def run(
        self,
    ) -> list[StageResult]:
        """
        Execute the configured enterprise pipeline.
        """

        stages = self.context.config.pipeline.stages

        total_stages = len(stages)

        self.logger.info("=" * 79)
        self.logger.info("Enterprise Pipeline Execution Started")
        self.logger.info("=" * 79)

        for index, stage_name in enumerate(
            stages,
            start=1,
        ):

            self.logger.info(
                "[%s/%s] Executing Stage: %s",
                index,
                total_stages,
                stage_name,
            )

            stage = StageRegistry.get(stage_name)

            # -------------------------------------------------------------
            # Stage Setup
            # -------------------------------------------------------------

            self.context.set_stage(stage.name)

            stage.before_execute(
                self.context,
            )

            # -------------------------------------------------------------
            # Validate Stage
            # -------------------------------------------------------------

            if not stage.validate(
                self.context,
            ):

                result = StageResult(

                    stage_name=stage.name,

                    status=StageStatus.SKIPPED,

                    message="Stage validation failed.",

                )

                result.complete()

                self.results.append(
                    result,
                )

                self.logger.warning(
                    "Stage skipped: %s",
                    stage.name,
                )

                continue

            # -------------------------------------------------------------
            # Execute Stage
            # -------------------------------------------------------------

            try:

                result = stage.execute(
                    self.context,
                )

                result.complete()

                stage.after_execute(

                    self.context,

                    result,

                )

                self.results.append(
                    result,
                )

                self.logger.info(
                    "Stage completed successfully: %s",
                    stage.name,
                )

            # -------------------------------------------------------------
            # Failure
            # -------------------------------------------------------------

            except Exception as error:

                result = StageResult(

                    stage_name=stage.name,

                    status=StageStatus.FAILED,

                    message=str(error),

                )

                result.complete()

                self.results.append(
                    result,
                )

                self.logger.exception(
                    "Stage failed: %s",
                    stage.name,
                )

                #
                # Enterprise Fail-Fast Policy
                #
                raise

            # -------------------------------------------------------------
            # Cleanup
            # -------------------------------------------------------------

            finally:

                stage.cleanup(
                    self.context,
                )

        # ---------------------------------------------------------------------
        # Synchronize Execution Context
        # ---------------------------------------------------------------------

        self.context.total_stages = self.total_stages

        self.context.successful_stages = self.successful_stages

        self.context.failed_stages = self.failed_stages

        self.context.skipped_stages = self.skipped_stages

        self.context.rows_processed = self.total_rows_processed

        self.context.rows_loaded = self.total_rows_loaded

        self.context.execution_seconds = self.execution_seconds

        # ---------------------------------------------------------------------
        # Pipeline Summary
        # ---------------------------------------------------------------------

        self.logger.info("=" * 79)
        self.logger.info("Enterprise Pipeline Summary")
        self.logger.info("=" * 79)

        self.logger.info(
            "Stages Executed : %s",
            self.total_stages,
        )

        self.logger.info(
            "Successful      : %s",
            self.successful_stages,
        )

        self.logger.info(
            "Failed          : %s",
            self.failed_stages,
        )

        self.logger.info(
            "Skipped         : %s",
            self.skipped_stages,
        )

        self.logger.info(
            "Rows Processed  : %s",
            f"{self.total_rows_processed:,}",
        )

        self.logger.info(
            "Rows Loaded     : %s",
            f"{self.total_rows_loaded:,}",
        )

        self.logger.info(
            "Execution Time  : %.2f sec",
            self.execution_seconds,
        )

        self.logger.info("=" * 79)
        self.logger.info("Enterprise Pipeline Completed")
        self.logger.info("=" * 79)

        return self.results
    
    # =========================================================================
    # Pipeline Status
    # =========================================================================

    @property
    def succeeded(self) -> bool:
        """
        True when all executed stages completed successfully.
        """

        return (
            self.failed_stages == 0
            and self.successful_stages == self.total_stages
        )

    # -------------------------------------------------------------------------

    @property
    def failed(self) -> bool:
        """
        True when one or more stages failed.
        """

        return self.failed_stages > 0

    # -------------------------------------------------------------------------

    @property
    def healthy(self) -> bool:
        """
        Overall pipeline health.
        """

        return not self.failed

    # =========================================================================
    # Pipeline Statistics
    # =========================================================================

    @property
    def total_stages(self) -> int:
        """
        Total number of executed stages.
        """

        return len(self.results)

    # -------------------------------------------------------------------------

    @property
    def successful_stages(self) -> int:
        """
        Number of successful stages.
        """

        return sum(
            1
            for result in self.results
            if result.status == StageStatus.SUCCESS
        )

    # -------------------------------------------------------------------------

    @property
    def failed_stages(self) -> int:
        """
        Number of failed stages.
        """

        return sum(
            1
            for result in self.results
            if result.status == StageStatus.FAILED
        )

    # -------------------------------------------------------------------------

    @property
    def skipped_stages(self) -> int:
        """
        Number of skipped stages.
        """

        return sum(
            1
            for result in self.results
            if result.status == StageStatus.SKIPPED
        )

    # =========================================================================
    # Pipeline Metrics
    # =========================================================================

    @property
    def total_rows_processed(self) -> int:
        """
        Total rows processed across all executed stages.
        """

        return sum(
            result.rows_processed
            for result in self.results
        )

    # -------------------------------------------------------------------------

    @property
    def total_rows_loaded(self) -> int:
        """
        Total rows loaded across all executed stages.
        """

        return sum(
            result.rows_loaded
            for result in self.results
        )

    # -------------------------------------------------------------------------

    @property
    def execution_seconds(self) -> float:
        """
        Total pipeline execution time.
        """

        return round(
            sum(
                result.execution_seconds
                for result in self.results
            ),
            3,
        )

    # =========================================================================
    # Pipeline Summary
    # =========================================================================

    @property
    def summary(self) -> dict:
        """
        Enterprise pipeline execution summary.

        Returns
        -------
        dict
            Consolidated execution statistics for the pipeline.
        """

        return {

            "healthy": self.healthy,

            "succeeded": self.succeeded,

            "failed": self.failed,

            "total_stages": self.total_stages,

            "successful_stages": self.successful_stages,

            "failed_stages": self.failed_stages,

            "skipped_stages": self.skipped_stages,

            "rows_processed": self.total_rows_processed,

            "rows_loaded": self.total_rows_loaded,

            "execution_seconds": self.execution_seconds,

        }

    # =========================================================================
    # String Representation
    # =========================================================================

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"stages={self.total_stages}, "
            f"successful={self.successful_stages}, "
            f"failed={self.failed_stages}, "
            f"healthy={self.healthy})"
        )