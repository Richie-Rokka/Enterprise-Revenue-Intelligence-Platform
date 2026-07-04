"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Warehouse Manager

Public interface for all warehouse operations.

Responsibilities
----------------
- Deploy warehouse
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
2.1.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.observability import get_logger

from src.database.database_executor import (
    DatabaseExecutor,
    ExecutionResult,
)

from .registry import DDLRegistry
from .validator import (
    WarehouseValidator,
    ValidationResult,
)

logger = get_logger(__name__)


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


# =============================================================================
# Warehouse Manager
# =============================================================================

class WarehouseManager:
    """
    Enterprise Warehouse Manager.

    Public entry point for all warehouse operations.
    """

    def __init__(self) -> None:

        self.registry = DDLRegistry()

        self.executor = DatabaseExecutor()

        self.validator = WarehouseValidator()

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------

    def _run_operation(
        self,
        script_name: str,
    ) -> ExecutionResult:
        """
        Execute a warehouse operational SQL script.

        Parameters
        ----------
        script_name
            SQL filename located under sql/operations.

        Returns
        -------
        ExecutionResult
        """

        script_path = OPERATIONS_DIRECTORY / script_name

        logger.info(
            "Executing Warehouse Operation: %s",
            script_name,
        )

        return self.executor.execute(
            script_path=script_path,
            script_name=script_name,
        )

    # -------------------------------------------------------------------------
    # Deployment
    # -------------------------------------------------------------------------

    def rebuild(self) -> WarehouseDeploymentResult:
        """
        Build or rebuild the warehouse.
        """

        logger.info("=" * 60)
        logger.info("WAREHOUSE DEPLOYMENT STARTED")
        logger.info("=" * 60)

        self.registry.validate()

        execution_results = self.executor.execute_many(

            [script.path for script in self.registry]

        )

        validation = self.validator.validate()

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
    # Warehouse Operations
    # -------------------------------------------------------------------------

    def refresh(self) -> ExecutionResult:
        """
        Execute refresh_warehouse.sql.
        """

        return self._run_operation(
            "refresh_warehouse.sql"
        )

    def refresh_metadata(self) -> ExecutionResult:
        """
        Refresh warehouse metadata.
        """

        return self._run_operation(
            "refresh_metadata.sql"
        )

    def health(self) -> ExecutionResult:
        """
        Execute warehouse health checks.
        """

        return self._run_operation(
            "warehouse_health.sql"
        )

    def statistics(self) -> ExecutionResult:
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
        Validate warehouse.
        """

        return self.validator.validate()

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return warehouse status.
        """

        validation = self.validator.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------
    # Version
    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Return framework version.
        """

        return "2.1.0"