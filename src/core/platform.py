"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : platform.py
Package     : src.core
Purpose     : Platform Bootstrap & Lifecycle Management
Author      : ERIP
Version     : 2.1.0

Description
-----------
Bootstraps and executes the Enterprise Revenue Intelligence Platform.

Responsibilities
----------------
- Initialize shared services
- Build execution context
- Register pipeline stages
- Execute the pipeline
- Publish execution summary

===============================================================================
"""

from __future__ import annotations

from src.core.services import ServiceContainer

from src.orchestration.execution_context import ExecutionContext
from src.orchestration.pipeline import Pipeline
from src.orchestration.register_stages import register_stages

from src.observability import (
    Timer,
    PipelineSummary,
    get_memory_usage,
)


class Platform:
    """
    Enterprise Revenue Intelligence Platform.
    """

    def __init__(self) -> None:

        self.services = ServiceContainer()

    # ---------------------------------------------------------------------

    def run(self) -> None:
        """
        Execute the platform.
        """

        logger = self.services.logger
        config = self.services.config
        engine = self.services.engine

        logger.info("")
        logger.info("=" * 70)
        logger.info("Enterprise Revenue Intelligence Platform (ERIP)")
        logger.info("=" * 70)
        logger.info("Platform Initializing...")
        logger.info("")

        summary = PipelineSummary(
            pipeline_name=config.pipeline.name
        )

        try:

            with Timer() as timer:

                # ---------------------------------------------------------
                # Build Execution Context
                # ---------------------------------------------------------

                context = ExecutionContext(
                    platform_name="Enterprise Revenue Intelligence Platform",
                    platform_version="2.1.0",
                    pipeline_name=config.pipeline.name,
                    environment=config.pipeline.environment,
                    engine=engine,
                    logger=logger,
                    config=config,
                )

                # ---------------------------------------------------------
                # Register Pipeline Stages
                # ---------------------------------------------------------

                register_stages()

                logger.info("Stage Registry Loaded")

                # ---------------------------------------------------------
                # Execute Pipeline
                # ---------------------------------------------------------

                pipeline = Pipeline(context)

                results = pipeline.run()

            # ---------------------------------------------------------
            # Pipeline Summary
            # ---------------------------------------------------------

            summary.rows_processed = sum(
                result.rows_processed
                for result in results
            )

            summary.rows_loaded = sum(
                result.rows_loaded
                for result in results
            )

            summary.rows_failed = sum(
                result.errors
                for result in results
            )

            summary.execution_time_seconds = timer.elapsed_seconds

            memory = get_memory_usage()

            summary.memory_usage_mb = memory.current_mb

            summary.mark_success()

            logger.info("")
            logger.info(summary.format())
            logger.info("")
            logger.info("Platform Completed Successfully")
            logger.info("")

        except Exception as error:

            summary.mark_failed(str(error))

            memory = get_memory_usage()

            summary.memory_usage_mb = memory.current_mb

            logger.exception("Platform Execution Failed")

            logger.error("")
            logger.error(summary.format())
            logger.error("")

            raise