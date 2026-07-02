"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : manager.py
Package     : src.semantic
Purpose     : Semantic Layer Manager
Author      : ERIP
Version     : 2.0.0

Description
-----------
Public interface for all Semantic Layer operations.

Responsibilities
----------------
- Deploy semantic layer
- Validate semantic layer
- Report deployment status

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from src.observability import get_logger

# NOTE:
# Until we refactor the SQLExecutor into a shared component,
# we reuse the Warehouse executor.
from src.database.database_executor import (
    DatabaseExecutor,
    ExecutionResult,
)

from .registry import SemanticRegistry
from .validator import (
    SemanticValidator,
    ValidationResult,
)


logger = get_logger(__name__)


# =============================================================================
# Deployment Result
# =============================================================================


@dataclass(slots=True)
class SemanticDeploymentResult:
    """
    Overall semantic deployment result.
    """

    success: bool

    scripts_executed: int

    validation_passed: bool

    execution_results: list[ExecutionResult]

    validation_result: ValidationResult


# =============================================================================
# Semantic Manager
# =============================================================================


class SemanticManager:
    """
    Enterprise Semantic Manager.

    Public interface for semantic deployment.
    """

    def __init__(self) -> None:

        self.registry = SemanticRegistry()

        self.executor = DatabaseExecutor()

        self.validator = SemanticValidator()

    # -------------------------------------------------------------------------

    def rebuild(self) -> SemanticDeploymentResult:
        """
        Deploy the complete semantic layer.
        """

        logger.info("=" * 60)
        logger.info("SEMANTIC LAYER DEPLOYMENT STARTED")
        logger.info("=" * 60)

        # ---------------------------------------------------------
        # Validate Registry
        # ---------------------------------------------------------

        self.registry.validate()

        # ---------------------------------------------------------
        # Execute SQL
        # ---------------------------------------------------------

        execution_results = self.executor.execute_many(

            [script.path for script in self.registry]

        )

        # ---------------------------------------------------------
        # Validate Semantic Layer
        # ---------------------------------------------------------

        validation = self.validator.validate()

        success = validation.passed

        if success:

            logger.info("=" * 60)
            logger.info("SEMANTIC LAYER DEPLOYMENT SUCCEEDED")
            logger.info("=" * 60)

        else:

            logger.error("=" * 60)
            logger.error("SEMANTIC LAYER DEPLOYMENT FAILED")
            logger.error("=" * 60)

            for failure in validation.failures:

                logger.error(failure)

        return SemanticDeploymentResult(

            success=success,

            scripts_executed=len(execution_results),

            validation_passed=validation.passed,

            execution_results=execution_results,

            validation_result=validation,
        )

    # -------------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Validate semantic layer.
        """

        return self.validator.validate()

    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return semantic deployment status.
        """

        validation = self.validator.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Framework version.
        """

        return "2.0.0"