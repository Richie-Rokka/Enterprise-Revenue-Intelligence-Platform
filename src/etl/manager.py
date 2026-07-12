"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : manager.py
Package     : src.etl
Purpose     : Enterprise ETL Orchestrator
Author      : ERIP
Version     : 3.0.0

Description
-----------
Coordinates the complete ETL lifecycle.

Responsibilities
----------------
• Extract source data
• Transform datasets
• Validate transformed data
• Load curated data
• Collect execution metrics
• Return execution summary

Notes
-----
The ETL Manager contains no dataset-specific logic.

Individual pipelines implement the Extract, Transform,
Validate and Load components.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from src.etl.dataset_registry import DatasetRegistry
from src.etl.results import PipelineResult

from src.observability import get_logger


logger = get_logger(__name__)


# =============================================================================
# ETL Summary
# =============================================================================

@dataclass(slots=True)
class ETLSummary:
    """
    Standard ETL execution summary.
    """

    extracted_rows: int = 0

    transformed_rows: int = 0

    validated_rows: int = 0

    loaded_rows: int = 0

    failed_rows: int = 0


# =============================================================================
# ETL Manager
# =============================================================================

class ETLManager:
    """
    Enterprise ETL Orchestrator.
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.summary = ETLSummary()

        self.pipeline_results: list[PipelineResult] = []

    # -------------------------------------------------------------------------

    def run_pipeline(self) -> ETLSummary:
        """
        Execute all registered ETL pipelines.
        """

        logger.info("=" * 60)
        logger.info("ETL PIPELINE STARTED")
        logger.info("=" * 60)

        self.summary = ETLSummary()

        self.pipeline_results.clear()

        DatasetRegistry.register_all()

        for dataset_name in DatasetRegistry.registered_datasets():

            logger.info(
                "Executing pipeline: %s",
                dataset_name,
            )

            pipeline = DatasetRegistry.build_pipeline(
                dataset_name
            )

            result = pipeline.execute()

            self.pipeline_results.append(
                result
            )

            self.summary.extracted_rows += (
                result.rows_extracted
            )

            self.summary.transformed_rows += (
                result.rows_transformed
            )

            self.summary.validated_rows += (
                result.rows_validated
            )

            self.summary.loaded_rows += (
                result.load_result.rows_loaded
            )

        logger.info("=" * 60)
        logger.info("ETL PIPELINE COMPLETED")
        logger.info("=" * 60)

        return self.summary

    # -------------------------------------------------------------------------


   