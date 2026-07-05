"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : platform.py
Package     : src.core
Purpose     : Enterprise Platform Bootstrap & Lifecycle Management
Author      : ERIP
Version     : 2.2.1

Description
-----------
Enterprise Platform Facade.

Responsibilities
----------------
- Bootstrap the ERIP platform
- Execute orchestration pipeline
- Deploy platform components
- Validate platform
- Report platform health
- Refresh platform metadata
- Publish execution summary

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.services import ServiceContainer

from src.orchestration.execution_context import ExecutionContext
from src.orchestration.pipeline import Pipeline
from src.orchestration.register_stages import register_stages

from src.observability import (
    Timer,
    PipelineSummary,
    get_memory_usage,
)

from src.warehouse.manager import WarehouseDeploymentResult
from src.semantic.manager import SemanticDeploymentResult

from src.warehouse.validator import ValidationResult as WarehouseValidationResult
from src.semantic.validator import ValidationResult as SemanticValidationResult

from src.database.database_executor import ExecutionResult

from src.warehouse.manager import (
    WarehouseDeploymentResult,
    WarehouseLoadResult,
)

from src.semantic.manager import (
    SemanticDeploymentResult,
)


# =============================================================================
# Platform Results
# =============================================================================


@dataclass(slots=True)
class PlatformDeploymentResult:
    """
    Overall platform deployment result.
    """

    success: bool

    warehouse_success: bool

    warehouse_load_success: bool

    metadata_refresh_success: bool

    semantic_success: bool

    warehouse_result: WarehouseDeploymentResult

    warehouse_load_result: WarehouseLoadResult

    metadata_refresh_result: ExecutionResult

    semantic_result: SemanticDeploymentResult


@dataclass(slots=True)
class PlatformValidationResult:
    """
    Platform validation result.
    """

    passed: bool

    warehouse_passed: bool

    semantic_passed: bool

    failures: list[str]


@dataclass(slots=True)
class PlatformHealth:
    """
    Platform health report.
    """

    database: str

    warehouse: str

    semantic: str

    overall: str


# =============================================================================
# Platform
# =============================================================================


class Platform:
    """
    Enterprise Revenue Intelligence Platform.

    Public facade for all platform operations.
    """

    VERSION = "2.2.1"

    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self.services = ServiceContainer()

    # -------------------------------------------------------------------------
    # Pipeline Execution
    # -------------------------------------------------------------------------

    def run(self) -> None:
        """
        Execute the Enterprise Revenue Intelligence Platform.
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

                    platform_version=self.VERSION,

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

    # -------------------------------------------------------------------------
    # Platform Deployment
    # -------------------------------------------------------------------------

    def deploy(self) -> PlatformDeploymentResult:
        """
        Deploy the complete Enterprise Revenue Intelligence Platform.
        """

        logger = self.services.logger

        logger.info("=" * 70)
        logger.info("ERIP PLATFORM DEPLOYMENT STARTED")
        logger.info("=" * 70)

        # ---------------------------------------------------------
        # Warehouse DDL
        # ---------------------------------------------------------

        warehouse_result = (

            self.services.warehouse_manager.rebuild()

        )

        # ---------------------------------------------------------
        # Warehouse Load
        # ---------------------------------------------------------

        warehouse_load = (

            self.services.warehouse_manager.load()

        )

        # ---------------------------------------------------------
        # Metadata Refresh
        # ---------------------------------------------------------

        metadata_refresh = (

            self.services.warehouse_manager.refresh_metadata()

        )

        # ---------------------------------------------------------
        # Semantic Layer
        # ---------------------------------------------------------

        semantic_result = (

            self.services.semantic_manager.deploy()

        )

        success = (

            warehouse_result.success

            and warehouse_load.success

            and metadata_refresh.success

            and semantic_result.success

        )

        if success:

            logger.info("=" * 70)
            logger.info("ERIP PLATFORM DEPLOYMENT SUCCEEDED")
            logger.info("=" * 70)

        else:

            logger.error("=" * 70)
            logger.error("ERIP PLATFORM DEPLOYMENT FAILED")
            logger.error("=" * 70)

        return PlatformDeploymentResult(

            success=success,

            warehouse_success=warehouse_result.success,

            warehouse_load_success=warehouse_load.success,

            metadata_refresh_success=metadata_refresh.success,

            semantic_success=semantic_result.success,

            warehouse_result=warehouse_result,

            warehouse_load_result=warehouse_load,

            metadata_refresh_result=metadata_refresh,

            semantic_result=semantic_result,

        )
    
    # -------------------------------------------------------------------------
    # Platform Refresh
    # -------------------------------------------------------------------------

    def refresh(self) -> PlatformValidationResult:
        """
        Refresh the Enterprise Revenue Intelligence Platform.

        Refresh performs operational maintenance without rebuilding
        the warehouse schema.

        Steps
        -----
        1. Reload warehouse dimensions and facts
        2. Refresh warehouse metadata
        3. Refresh semantic layer
        4. Validate the platform

        Returns
        -------
        PlatformValidationResult
        """

        logger = self.services.logger

        logger.info("=" * 70)
        logger.info("ERIP PLATFORM REFRESH STARTED")
        logger.info("=" * 70)

        # ---------------------------------------------------------
        # Reload Warehouse Data
        # ---------------------------------------------------------

        self.services.warehouse_manager.load()

        # ---------------------------------------------------------
        # Refresh Metadata
        # ---------------------------------------------------------

        self.services.warehouse_manager.refresh_metadata()

        # ---------------------------------------------------------
        # Refresh Semantic Layer
        # ---------------------------------------------------------

        self.services.semantic_manager.refresh()

        # ---------------------------------------------------------
        # Validate Platform
        # ---------------------------------------------------------

        validation = self.validate()

        if validation.passed:

            logger.info("=" * 70)
            logger.info("ERIP PLATFORM REFRESH SUCCEEDED")
            logger.info("=" * 70)

        else:

            logger.error("=" * 70)
            logger.error("ERIP PLATFORM REFRESH FAILED")
            logger.error("=" * 70)

        return validation

    # -------------------------------------------------------------------------
    # Platform Validation
    # -------------------------------------------------------------------------

    def validate(self) -> PlatformValidationResult:
        """
        Validate the complete platform.
        """

        warehouse_validation = (

            self.services.warehouse_manager.validate()

        )

        semantic_validation = (

            self.services.semantic_manager.validate()

        )

        failures: list[str] = []

        failures.extend(

            warehouse_validation.failures

        )

        failures.extend(

            semantic_validation.failures

        )

        passed = (

            warehouse_validation.passed

            and

            semantic_validation.passed

        )

        return PlatformValidationResult(

            passed=passed,

            warehouse_passed=warehouse_validation.passed,

            semantic_passed=semantic_validation.passed,

            failures=failures,

        )

    # -------------------------------------------------------------------------
    # Platform Health
    # -------------------------------------------------------------------------

    def health(self) -> PlatformHealth:
        """
        Return Enterprise Platform health.
        """

        warehouse_status = (

            self.services.warehouse_manager.status()

        )

        semantic_status = (

            self.services.semantic_manager.status()

        )

        database_status = "READY"

        overall = (

            "HEALTHY"

            if (

                database_status == "READY"

                and warehouse_status == "READY"

                and semantic_status == "READY"

            )

            else "UNHEALTHY"

        )

        return PlatformHealth(

            database=database_status,

            warehouse=warehouse_status,

            semantic=semantic_status,

            overall=overall,

        )

    # -------------------------------------------------------------------------
    # Platform Status
    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return platform status.
        """

        validation = self.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------
    # Framework Version
    # -------------------------------------------------------------------------

    @classmethod
    def version(cls) -> str:
        """
        Return platform version.
        """

        return cls.VERSION