"""
Enterprise Revenue Intelligence Platform (ERIP)

Warehouse Manager

Public interface for all warehouse operations.

Responsibilities
----------------
- Deploy warehouse
- Validate warehouse
- Report deployment status
"""

from __future__ import annotations

from dataclasses import dataclass

from src.observability import get_logger

from .executor import SQLExecutor, ExecutionResult
from .registry import DDLRegistry
from .validator import WarehouseValidator, ValidationResult


logger = get_logger(__name__)


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


class WarehouseManager:
    """
    Enterprise Warehouse Manager.

    This class is the public entry point for all
    warehouse operations.
    """

    def __init__(self) -> None:

        self.registry = DDLRegistry()

        self.executor = SQLExecutor()

        self.validator = WarehouseValidator()

    def rebuild(self) -> WarehouseDeploymentResult:
        """
        Build or rebuild the warehouse.

        Returns
        -------
        WarehouseDeploymentResult
        """

        logger.info("=" * 60)
        logger.info("WAREHOUSE DEPLOYMENT STARTED")
        logger.info("=" * 60)

        # ------------------------------------------
        # Validate Registry
        # ------------------------------------------

        self.registry.validate()

        # ------------------------------------------
        # Execute SQL
        # ------------------------------------------

        execution_results = self.executor.execute_all(

            list(self.registry)

        )

        # ------------------------------------------
        # Validate Warehouse
        # ------------------------------------------

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

    def validate(self) -> ValidationResult:
        """
        Validate warehouse only.
        """

        return self.validator.validate()

    def status(self) -> str:
        """
        Return warehouse status.
        """

        validation = self.validator.validate()

        return "READY" if validation.passed else "INVALID"

    def version(self) -> str:
        """
        Return framework version.
        """

        return "2.0.0"