"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : manager.py
Package     : src.monitoring
Purpose     : Enterprise Monitoring Manager

Author      : ERIP
Version     : 3.0.0

Description
-----------
Enterprise Monitoring Framework Manager.

Provides the public interface for all monitoring operations and coordinates
platform monitoring through the Enterprise Runtime Framework.

Responsibilities
----------------
• Platform health
• Runtime metrics
• Warehouse statistics
• Enterprise dashboard
• Monitoring validation
• Framework status

Architecture
------------
Monitoring is an Enterprise Coordination Framework.

Unlike the Warehouse and Semantic frameworks, Monitoring primarily aggregates
information from other frameworks rather than deploying database objects.

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from src.database.database_executor import (
    DatabaseExecutor,
    ExecutionResult,
)

from src.observability import get_logger

from src.runtime.manager import RuntimeManager
from src.runtime.models import FrameworkState

from src.semantic.manager import SemanticManager
from src.warehouse.manager import WarehouseManager

from .models import (
    DeploymentStatistics,
    MonitoringDashboard,
    MonitoringValidationResult,
    PlatformHealth,
    RuntimeStatistics,
    SemanticStatistics,
    WarehouseStatistics,
)

from .registry import MonitoringRegistry
from .validator import MonitoringValidator


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OPERATIONS_DIRECTORY = (
    PROJECT_ROOT
    / "sql"
    / "operations"
)

logger = get_logger(__name__)


# =============================================================================
# Monitoring Manager
# =============================================================================


class MonitoringManager:
    """
    Enterprise Monitoring Manager.

    Coordinates enterprise monitoring across all platform frameworks.

    The Monitoring Manager is responsible for:

    • Platform health
    • Runtime metrics
    • Monitoring dashboard
    • Operational statistics
    • Monitoring validation

    Monitoring is intentionally lightweight and acts as an orchestration
    layer rather than a deployment framework.
    """

    VERSION = "3.0.0"

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(
        self,
        *,
        registry: MonitoringRegistry,
        validator: MonitoringValidator,
        executor: DatabaseExecutor,
        warehouse: WarehouseManager,
        semantic: SemanticManager,
        runtime: RuntimeManager,
    ) -> None:
        """
        Construct the Enterprise Monitoring Manager.
        """

        # ---------------------------------------------------------------------
        # Shared Dependencies
        # ---------------------------------------------------------------------

        self.registry = registry

        self.validator = validator

        self.executor = executor

        self.warehouse = warehouse

        self.semantic = semantic

        self.runtime = runtime

        # ---------------------------------------------------------------------
        # Cached State
        # ---------------------------------------------------------------------

        self._validation_result: MonitoringValidationResult | None = None

        self._validation_dirty = True

    # =========================================================================
    # Public API
    # =========================================================================

    def health(
        self,
    ) -> PlatformHealth:
        """
        Return overall enterprise platform health.
        """

        return self._health()

    # -------------------------------------------------------------------------

    def metrics(
        self,
    ) -> RuntimeStatistics:
        """
        Return enterprise runtime metrics.
        """

        return self._metrics()

    # -------------------------------------------------------------------------

    def statistics(
        self,
    ) -> ExecutionResult:
        """
        Execute Monitoring statistics under Runtime control.
        """

        self.runtime.begin(

            framework="Monitoring",

            operation="Statistics",

        )

        self.runtime.state(

            FrameworkState.VALIDATING

        )

        try:

            result = self._statistics()

            self.runtime.success()

            return result

        except Exception as exc:

            self.runtime.failure(

                exc

            )

            raise

    # -------------------------------------------------------------------------

    def dashboard(
        self,
    ) -> MonitoringDashboard:
        """
        Build the Enterprise Monitoring Dashboard.
        """

        return self._dashboard()

    # -------------------------------------------------------------------------

    def validate(
        self,
    ) -> MonitoringValidationResult:
        """
        Validate the Monitoring Framework.

        Validation results are cached until the monitoring state changes.
        """

        return self._validate()

    # -------------------------------------------------------------------------

    def status(
        self,
    ) -> str:
        """
        Return Monitoring Framework status.
        """

        validation = self.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------

    @classmethod
    def version(
        cls,
    ) -> str:
        """
        Return framework version.
        """

        return cls.VERSION

    # =========================================================================
    # Private Operations
    # =========================================================================

    def _health(
        self,
    ) -> PlatformHealth:
        """
        Build the Enterprise Platform Health model.
        """

        warehouse_status = self.warehouse.status()

        semantic_status = self.semantic.status()

        overall = (

            "HEALTHY"

            if (

                warehouse_status == "READY"

                and

                semantic_status == "READY"

            )

            else "UNHEALTHY"

        )

        return PlatformHealth(

            database="CONNECTED",

            warehouse=warehouse_status,

            semantic=semantic_status,

            overall=overall,

        )

    # -------------------------------------------------------------------------

    def _metrics(
        self,
    ) -> RuntimeStatistics:
        """
        Build Runtime statistics.

        Runtime metrics will become richer in a future sprint when Runtime
        telemetry is expanded.
        """

        return RuntimeStatistics(

            execution_time_seconds=0.0,

            memory_usage_mb=0.0,

        )

    # -------------------------------------------------------------------------

    def _statistics(
        self,
    ) -> ExecutionResult:
        """
        Execute enterprise Monitoring statistics.
        """

        logger.info(

            "Executing Monitoring Operation: monitoring_statistics.sql"

        )

        return self.executor.execute(

            script_path=(

                OPERATIONS_DIRECTORY

                / "monitoring_statistics.sql"

            ),

            script_name="monitoring_statistics.sql",

        )

    # -------------------------------------------------------------------------

    def _dashboard(
        self,
    ) -> MonitoringDashboard:
        """
        Build the Enterprise Monitoring Dashboard.
        """

        health = self._health()

        runtime = self._metrics()

        deployment = DeploymentStatistics(

            deployment_success=True,

            scripts_executed=0,

            execution_time_seconds=0.0,

        )

        warehouse = WarehouseStatistics(

            dimensions_loaded=4,

            fact_tables_loaded=1,

            rows_processed=112650,

            execution_time_seconds=0.0,

        )

        semantic = SemanticStatistics(

            views_deployed=5,

            validation_checks=4,

            deployment_success=True,

            execution_time_seconds=0.0,

        )

        return MonitoringDashboard(

            platform_health=health,

            runtime=runtime,

            deployment=deployment,

            warehouse=warehouse,

            semantic=semantic,

        )

    # -------------------------------------------------------------------------

    def _validate(
        self,
    ) -> MonitoringValidationResult:
        """
        Validate the Monitoring Framework.
        """

        if self._validation_dirty:

            logger.info(

                "Starting Monitoring validation..."

            )

            self._validation_result = (

                self.validator.validate()

            )

            self._validation_dirty = False

        return self._validation_result

    # =========================================================================
    # Dashboard Helpers
    # =========================================================================

    def _warehouse_statistics(
        self,
    ) -> WarehouseStatistics:
        """
        Build Warehouse statistics.

        TODO
        ----
        Replace placeholder values with Runtime telemetry during the
        Observability enhancement sprint.
        """

        return WarehouseStatistics(

            dimensions_loaded=4,

            fact_tables_loaded=1,

            rows_processed=112650,

            execution_time_seconds=0.0,

        )

    # -------------------------------------------------------------------------

    def _semantic_statistics(
        self,
    ) -> SemanticStatistics:
        """
        Build Semantic statistics.

        TODO
        ----
        Replace placeholder values with Semantic runtime metrics.
        """

        return SemanticStatistics(

            views_deployed=5,

            validation_checks=4,

            deployment_success=True,

            execution_time_seconds=0.0,

        )

    # -------------------------------------------------------------------------

    def _deployment_statistics(
        self,
    ) -> DeploymentStatistics:
        """
        Build deployment statistics.

        TODO
        ----
        Populate from Runtime execution history when deployment telemetry
        becomes available.
        """

        return DeploymentStatistics(

            deployment_success=True,

            scripts_executed=0,

            execution_time_seconds=0.0,

        )