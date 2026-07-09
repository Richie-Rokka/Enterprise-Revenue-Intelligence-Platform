"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Warehouse Manager

Public interface for all warehouse operations.

Responsibilities
----------------
- Deploy warehouse
- Load warehouse
- Refresh warehouse
- Refresh metadata
- Validate warehouse
- Execute operational SQL services
- Report warehouse status
- Report framework version

Author
------
ERIP

Version
-------
3.0.0
===============================================================================
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import TypeVar

from src.database.database_executor import (
    DatabaseExecutor,
    ExecutionResult,
)
from src.observability import get_logger
from src.runtime.manager import RuntimeManager
from src.runtime.models import FrameworkState

from .registry import DDLRegistry
from .validator import (
    ValidationResult,
    WarehouseValidator,
)

logger = get_logger(__name__)

T = TypeVar("T")


# =============================================================================
# Constants
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OPERATIONS_DIRECTORY = PROJECT_ROOT / "sql" / "operations"


# =============================================================================
# Deployment Result
# =============================================================================


@dataclass(slots=True)
class WarehouseDeploymentResult:
    """
    Overall warehouse deployment result.
    """

    success: bool

    scripts_executed: int

    validation_passed: bool

    execution_results: list[ExecutionResult]

    validation_result: ValidationResult


@dataclass(slots=True)
class WarehouseLoadStep:
    """
    Individual warehouse load step.
    """

    procedure: str

    success: bool

    execution_time_seconds: float

    error: str | None = None


@dataclass(slots=True)
class WarehouseLoadResult:
    """
    Warehouse load summary.
    """

    success: bool

    procedures_executed: int

    execution_time_seconds: float

    steps: list[WarehouseLoadStep]


# =============================================================================
# Warehouse Manager
# =============================================================================


class WarehouseManager:
    """
    Enterprise Warehouse Manager.

    Public façade for all warehouse services.
    """

    VERSION = "3.0.0"

    FRAMEWORK = "Warehouse"

    LOAD_SEQUENCE = (

        (
            "Date Dimension",
            "CALL analytics.load_dim_date({start_year}, {end_year});",
        ),

        (
            "Product Dimension",
            "CALL analytics.load_dim_product();",
        ),

        (
            "Seller Dimension",
            "CALL analytics.load_dim_seller();",
        ),

        (
            "Customer Dimension",
            "CALL analytics.load_dim_customer();",
        ),

        (
            "Fact Sales",
            "CALL analytics.load_fact_sales();",
        ),

    )

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *,
        registry: DDLRegistry,
        validator: WarehouseValidator,
        executor: DatabaseExecutor,
        runtime: RuntimeManager,
    ) -> None:
        """
        Construct the Enterprise Warehouse Manager.
        """

        self.registry = registry

        self.validator = validator

        self.executor = executor

        self.runtime = runtime

        # ---------------------------------------------------------------------
        # Cached Validation
        # ---------------------------------------------------------------------

        self._validation_result: ValidationResult | None = None

        self._validation_dirty = True

    # -------------------------------------------------------------------------
    # Runtime Template
    # -------------------------------------------------------------------------

    def _execute_runtime_operation(
        self,
        *,
        operation: str,
        state: FrameworkState,
        action: Callable[[], T],
    ) -> T:
        """
        Execute a warehouse operation under Runtime control.
        """

        self.runtime.begin(

            framework=self.FRAMEWORK,

            operation=operation,

        )

        self.runtime.state(state)

        try:

            result = action()

            self.runtime.success()

            return result

        except Exception as exc:

            self.runtime.failure(exc)

            raise

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _run_operation(
        self,
        script_name: str,
    ) -> ExecutionResult:
        """
        Execute an operational SQL script.
        """

        script_path = OPERATIONS_DIRECTORY / script_name

        logger.info(

            "Executing Warehouse Operation: %s",

            script_name,

        )

        result = self.executor.execute(

            script_path=script_path,

            script_name=script_name,

        )

        self.runtime.add_rows_processed(

            result.rows_processed

        )

        return result

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def rebuild(self) -> WarehouseDeploymentResult:
        """
        Build or rebuild the warehouse.
        """

        return self._execute_runtime_operation(

            operation="Deploy",

            state=FrameworkState.DEPLOYING,

            action=self._rebuild,

        )

    # -------------------------------------------------------------------------

    def load(
        self,
        start_year: int = 2016,
        end_year: int = 2018,
    ) -> WarehouseLoadResult:
        """
        Load all warehouse dimensions and fact tables.
        """

        return self._execute_runtime_operation(

            operation="Load",

            state=FrameworkState.LOADING,

            action=lambda: self._load(

                start_year,

                end_year,

            ),

        )

    # -------------------------------------------------------------------------

    def refresh(self) -> ExecutionResult:
        """
        Refresh the warehouse.
        """

        return self._execute_runtime_operation(

            operation="Refresh",

            state=FrameworkState.REFRESHING,

            action=self._refresh,

        )

    # -------------------------------------------------------------------------

    def refresh_metadata(self) -> ExecutionResult:
        """
        Refresh warehouse metadata.
        """

        return self._execute_runtime_operation(

            operation="Refresh Metadata",

            state=FrameworkState.REFRESHING,

            action=self._refresh_metadata,

        )

    # -------------------------------------------------------------------------

    def health(self) -> ExecutionResult:
        """
        Execute warehouse health checks.
        """

        return self._execute_runtime_operation(

            operation="Health Check",

            state=FrameworkState.VALIDATING,

            action=self._health,

        )

    # -------------------------------------------------------------------------

    def statistics(self) -> ExecutionResult:
        """
        Generate warehouse statistics.
        """

        return self._execute_runtime_operation(

            operation="Statistics",

            state=FrameworkState.VALIDATING,

            action=self._statistics,

        )

    # =========================================================================
    # Private Business Logic
    # =========================================================================

    # -------------------------------------------------------------------------
    # Deployment
    # -------------------------------------------------------------------------

    def _rebuild(self) -> WarehouseDeploymentResult:
        """
        Build or rebuild the warehouse.
        """

        self._validation_dirty = True

        logger.info("=" * 60)
        logger.info("WAREHOUSE DEPLOYMENT STARTED")
        logger.info("=" * 60)

        self.registry.validate()

        execution_results = self.executor.execute_many(

            [script.path for script in self.registry]

        )

        self.runtime.state(

            FrameworkState.VALIDATING

        )

        validation = self.validate()

        success = validation.passed

        if success:

            logger.info("=" * 60)
            logger.info("WAREHOUSE DEPLOYMENT SUCCEEDED")
            logger.info("=" * 60)

        else:

            logger.error("=" * 60)
            logger.error("WAREHOUSE DEPLOYMENT FAILED")
            logger.error("=" * 60)

            for failure in validation.failures:

                logger.error(failure)

        return WarehouseDeploymentResult(

            success=success,

            scripts_executed=len(execution_results),

            validation_passed=validation.passed,

            execution_results=execution_results,

            validation_result=validation,

        )

    # -------------------------------------------------------------------------
    # Warehouse Load
    # -------------------------------------------------------------------------

    def _load(
        self,
        start_year: int,
        end_year: int,
    ) -> WarehouseLoadResult:
        """
        Load all warehouse dimensions and fact tables.
        """

        self._validation_dirty = True

        logger.info("=" * 60)
        logger.info("WAREHOUSE DATA LOAD STARTED")
        logger.info("=" * 60)

        started = perf_counter()

        steps: list[WarehouseLoadStep] = []

        total_rows_processed = 0

        for name, sql_template in self.LOAD_SEQUENCE:

            sql = sql_template.format(

                start_year=start_year,

                end_year=end_year,

            )

            logger.info(

                "Loading %s...",

                name,

            )

            result = self.executor.execute_sql(

                sql,

                operation_name=name,

            )

            steps.append(

                WarehouseLoadStep(

                    procedure=name,

                    success=result.success,

                    execution_time_seconds=result.execution_time_seconds,

                    error=result.error,

                )

            )

            if result.success:

                total_rows_processed += result.rows_processed

            if not result.success:

                logger.error(

                    "Warehouse Load Failed: %s",

                    name,

                )

                return WarehouseLoadResult(

                    success=False,

                    procedures_executed=len(steps),

                    execution_time_seconds=(

                        perf_counter() - started

                    ),

                    steps=steps,

                )

        self.runtime.add_rows_processed(

            total_rows_processed

        )

        logger.info("=" * 60)
        logger.info("WAREHOUSE DATA LOAD COMPLETED")
        logger.info("=" * 60)

        return WarehouseLoadResult(

            success=True,

            procedures_executed=len(steps),

            execution_time_seconds=(

                perf_counter() - started

            ),

            steps=steps,

        )

    # -------------------------------------------------------------------------
    # Warehouse Operations
    # -------------------------------------------------------------------------

    def _refresh(
        self,
    ) -> ExecutionResult:
        """
        Execute refresh_warehouse.sql.
        """

        self._validation_dirty = True

        result = self._run_operation(

            "refresh_warehouse.sql"

        )

    #
    # Refresh the cached validation after a successful refresh.
    #

        if result.success:

            self.validate()

        return result

    # -------------------------------------------------------------------------

    def _refresh_metadata(self) -> ExecutionResult:
        """
        Refresh warehouse metadata.
        """

        self._validation_dirty = True

        return self._run_operation(

            "refresh_metadata.sql"

        )

    # -------------------------------------------------------------------------

    def _health(self) -> ExecutionResult:
        """
        Execute warehouse health checks.
        """

        return self._run_operation(

            "warehouse_health.sql"

        )

    # -------------------------------------------------------------------------

    def _statistics(self) -> ExecutionResult:
        """
        Generate warehouse statistics.
        """

        return self._run_operation(

            "warehouse_statistics.sql"

        )

        # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Validate the warehouse.

        Returns
        -------
        ValidationResult
            Cached validation result.
        """

        if self._validation_dirty:

            self._validation_result = self.validator.validate()

            self._validation_dirty = False

        return self._validation_result

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return warehouse status.
        """

        validation = self.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------
    # Version
    # -------------------------------------------------------------------------

    @classmethod
    def version(cls) -> str:
        """
        Return framework version.
        """

        return cls.VERSION