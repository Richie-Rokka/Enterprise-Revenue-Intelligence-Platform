"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : platform.py
Package     : src.core
Purpose     : Enterprise Platform Bootstrap & Lifecycle Management
Author      : ERIP
Version     : 3.0.0

Description
-----------
Enterprise Platform Facade.

Responsibilities
----------------
- Bootstrap the ERIP platform
- Execute orchestration pipeline
- Deploy enterprise frameworks
- Validate platform
- Monitor platform health
- Refresh platform
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

from src.database.database_executor import ExecutionResult

from src.warehouse.manager import (
    WarehouseDeploymentResult,
    WarehouseLoadResult,
)

from src.semantic.manager import (
    SemanticDeploymentResult,
)

from src.warehouse.validator import (
    ValidationResult as WarehouseValidationResult,
)

from src.semantic.validator import (
    ValidationResult as SemanticValidationResult,
)

from src.quality.models import (
    DataQualityValidationResult as QualityValidationResult,
)

from src.monitoring.models import (
    MonitoringValidationResult,
)


# =============================================================================
# Platform Results
# =============================================================================


@dataclass(slots=True)
class PlatformDeploymentResult:
    """
    Overall ERIP deployment result.
    """

    success: bool

    warehouse_success: bool

    warehouse_load_success: bool

    metadata_refresh_success: bool

    semantic_success: bool

    quality_success: bool

    monitoring_success: bool

    warehouse_result: WarehouseDeploymentResult

    warehouse_load_result: WarehouseLoadResult

    metadata_refresh_result: ExecutionResult

    semantic_result: SemanticDeploymentResult

    quality_result: QualityValidationResult

    monitoring_result: MonitoringValidationResult


@dataclass(slots=True)
class PlatformValidationResult:
    """
    Overall platform validation.
    """

    passed: bool

    warehouse_passed: bool

    semantic_passed: bool

    quality_passed: bool

    monitoring_passed: bool

    failures: list[str]


@dataclass(slots=True)
class PlatformHealth:
    """
    Enterprise platform health.
    """

    database: str

    warehouse: str

    semantic: str

    quality: str

    monitoring: str

    runtime: str

    overall: str


# =============================================================================
# Platform
# =============================================================================


class Platform:
    """
    Enterprise Revenue Intelligence Platform.

    Enterprise facade responsible for coordinating all
    platform frameworks and lifecycle operations.
    """

    VERSION = "3.0.0"

    # ------------------------------------------------------------------ #

    def __init__(self) -> None:

        self.services = ServiceContainer()

    # -----------------------------------------------------------------------------
    # Pipeline Execution
    # -----------------------------------------------------------------------------

    def run(self) -> None:
        """
        Execute the complete Enterprise Revenue Intelligence Platform.
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

            pipeline_name=config.pipeline.name,

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

                services=self.services,

            )

            # ---------------------------------------------------------
            # Register Pipeline Stages
            # ---------------------------------------------------------

                register_stages()

                logger.info("Stage Registry Loaded")

            # ---------------------------------------------------------
            # Execute Enterprise Pipeline
            # ---------------------------------------------------------

                pipeline = Pipeline(context)

                results = pipeline.run()

            # ---------------------------------------------------------
            # Validate Platform
            # ---------------------------------------------------------
            
                validation = self.validate()
            
                if not validation.passed:
            
                    raise RuntimeError(
            
                        "Platform validation failed."
            
                    )
            
                logger.info("Platform Validation Successful")

            # ---------------------------------------------------------
            # Platform Summary
            # ---------------------------------------------------------

                summary.rows_processed = pipeline.total_rows_processed

                summary.rows_loaded = pipeline.total_rows_loaded

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

    # -----------------------------------------------------------------------------
    # Platform Deployment
    # -----------------------------------------------------------------------------

    def deploy(self) -> PlatformDeploymentResult:
        """
        Deploy the complete Enterprise Revenue Intelligence Platform.
        """

        logger = self.services.logger

        logger.info("=" * 70)
        logger.info("ERIP PLATFORM DEPLOYMENT STARTED")
        logger.info("=" * 70)

        # ---------------------------------------------------------
        # Warehouse Deployment
        # ---------------------------------------------------------

        warehouse_result = (

            self.services.warehouse_manager.rebuild()

        )

        warehouse_load_result = (

            self.services.warehouse_manager.load()

        )

        metadata_refresh_result = (

            self.services.warehouse_manager.refresh_metadata()

        )

        # ---------------------------------------------------------
        # Semantic Layer
        # ---------------------------------------------------------

        semantic_result = (

           self.services.semantic_manager.deploy()

        )

        # ---------------------------------------------------------
        # Quality Framework
        # ---------------------------------------------------------

        quality_result = (

            self.services.quality_manager.validate()

        )

        # ---------------------------------------------------------
        # Monitoring Framework
        # ---------------------------------------------------------

        monitoring_result = (

            self.services.monitoring_manager.validate()

        )

        # ---------------------------------------------------------
        # Overall Status
        # ---------------------------------------------------------

        success = (

           warehouse_result.success

           and warehouse_load_result.success

           and metadata_refresh_result.success

           and semantic_result.success

           and quality_result.passed

           and monitoring_result.passed

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

            warehouse_load_success=warehouse_load_result.success,

            metadata_refresh_success=metadata_refresh_result.success,

            semantic_success=semantic_result.success,

            quality_success=quality_result.passed,

            monitoring_success=monitoring_result.passed,

            warehouse_result=warehouse_result,

            warehouse_load_result=warehouse_load_result,

            metadata_refresh_result=metadata_refresh_result,

            semantic_result=semantic_result,

            quality_result=quality_result,

            monitoring_result=monitoring_result,

        )

    # -----------------------------------------------------------------------------
    # Platform Refresh
    # -----------------------------------------------------------------------------

    def refresh(self) -> PlatformValidationResult:
        """
        Refresh the Enterprise Revenue Intelligence Platform.
        """

        logger = self.services.logger

        logger.info("=" * 70)
        logger.info("ERIP PLATFORM REFRESH STARTED")
        logger.info("=" * 70)

        # ---------------------------------------------------------
        # Warehouse
        # ---------------------------------------------------------

        self.services.warehouse_manager.load()

        self.services.warehouse_manager.refresh_metadata()

        # ---------------------------------------------------------
        # Semantic
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


    # -----------------------------------------------------------------------------
    # Platform Validation
    # -----------------------------------------------------------------------------

    def validate(self) -> PlatformValidationResult:
        """
        Validate all enterprise platform frameworks.
        """

        warehouse_validation = (

            self.services.warehouse_manager.validate()

        )

        semantic_validation = (

            self.services.semantic_manager.validate()

        )

        quality_validation = (

            self.services.quality_manager.validate()

        )

        monitoring_validation = (

            self.services.monitoring_manager.validate()

        )

        failures: list[str] = []

        failures.extend(

            warehouse_validation.failures

        )

        failures.extend(

            semantic_validation.failures

        )

        failures.extend(

            quality_validation.failures

        )

        failures.extend(

            monitoring_validation.failures

        )

        passed = (

            warehouse_validation.passed

            and semantic_validation.passed

            and quality_validation.passed

            and monitoring_validation.passed

        )

        return PlatformValidationResult(

            passed=passed,

            warehouse_passed=warehouse_validation.passed,

            semantic_passed=semantic_validation.passed,

            quality_passed=quality_validation.passed,

            monitoring_passed=monitoring_validation.passed,

            failures=failures,

        )

    # -----------------------------------------------------------------------------
    # Platform Health
    # -----------------------------------------------------------------------------

    def health(self) -> PlatformHealth:
        """
        Return the Enterprise Platform health.
        """

        database_status = (

            self.services.database_health.status()

        )

        warehouse_status = (

            self.services.warehouse_manager.status()

        )

        semantic_status = (

            self.services.semantic_manager.status()

        )

        quality_status = (

            self.services.quality_manager.status()

        )

        monitoring_status = (

            self.services.monitoring_manager.status()

        )

        runtime_status = (

            self.services.runtime_manager.status()

        )

        overall = (

            "HEALTHY"

            if (

            database_status == "READY"

            and warehouse_status == "READY"

            and semantic_status == "READY"

            and quality_status == "READY"

            and monitoring_status == "READY"

            )

            else "UNHEALTHY"

        )

        return PlatformHealth(

            database=database_status,

            warehouse=warehouse_status,

            semantic=semantic_status,

            quality=quality_status,

            monitoring=monitoring_status,

            runtime=runtime_status,

            overall=overall,

        )


    # -----------------------------------------------------------------------------
    # Platform Status
    # -----------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return the current platform status.
        """

        return(

            "READY"

            if self.validate().passed

            else "INVALID"

        )


    # -----------------------------------------------------------------------------
    # Platform Initialize
    # -----------------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Initialize enterprise platform services.
        """

        logger = self.services.logger

        logger.info("=" * 70)
        logger.info("Initializing Enterprise Platform")
        logger.info("=" * 70)

        self.health()

        logger.info("Platform Initialization Complete")


    # -----------------------------------------------------------------------------
    # Platform Shutdown
    # -----------------------------------------------------------------------------

    def shutdown(self) -> None:
        """
        Shutdown enterprise platform.
        """

        logger = self.services.logger

        logger.info("=" * 70)
        logger.info("Shutting Down Enterprise Platform")
        logger.info("=" * 70)

        logger.info("Platform Shutdown Complete")


    # -----------------------------------------------------------------------------
    # Framework Version
    # -----------------------------------------------------------------------------

    @classmethod
    def version(cls) -> str:
        """
        Return platform version.
        """

        return cls.VERSION