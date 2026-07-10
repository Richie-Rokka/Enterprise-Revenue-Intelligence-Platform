"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : etl_stage.py
Package     : src.orchestration.stages
Purpose     : Enterprise ETL Pipeline Stage
Version     : 1.0.0
===============================================================================
"""

from __future__ import annotations

from src.orchestration.stage import Stage

from src.orchestration.stage_result import (
    StageResult,
    StageStatus,
)


class ETLStage(Stage):
    """
    Executes the Enterprise ETL Framework.
    """

    name = "etl"

    def execute(
        self,
        context,
    ):
       

        logger = context.logger

        logger.info("Starting ETL Stage...")

        manager = context.services.etl_manager

        summary = manager.run_pipeline()

        logger.info("ETL Stage Completed.")

        #
        # Adapt the ETL summary to the Pipeline contract.
        #

        result = StageResult(
            stage_name="etl",
           status=StageStatus.SUCCESS,
           message="ETL Pipeline completed successfully.",
        )

        if hasattr(summary, "rows_processed"):
            result.rows_processed = summary.rows_processed

        if hasattr(summary, "rows_loaded"):
            result.rows_loaded = summary.rows_loaded

        if hasattr(summary, "warnings"):
            result.warnings = summary.warnings

        if hasattr(summary, "errors"):
            result.errors = summary.errors

        result.add_metadata(
            "etl_summary",
            summary,
        )

        return result