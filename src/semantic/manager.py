"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : manager.py
Package     : src.semantic
Purpose     : Enterprise Semantic Layer Manager
Author      : ERIP
Version     : 2.3.0

Description
-----------
Public interface for all Semantic Layer operations.

Responsibilities
----------------
- Deploy semantic layer
- Refresh semantic layer
- Validate semantic layer
- Report semantic layer status
- Report framework version

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from src.observability import get_logger

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

    Public entry point for all Semantic Layer operations.
    """

    def __init__(self) -> None:

        self.registry = SemanticRegistry()

        self.executor = DatabaseExecutor()

        self.validator = SemanticValidator()

        # -----------------------------------------------------------------
        # Cached deployment state.
        #
        # The manager intentionally performs no database work during
        # construction. Validation is performed lazily when required.
        # -----------------------------------------------------------------

        self._is_deployed = False

    # -------------------------------------------------------------------------
    # Internal Deployment
    # -------------------------------------------------------------------------

    def _deploy(self) -> SemanticDeploymentResult:
        """
        Deploy the complete Semantic Layer.
        """

        logger.info("=" * 60)
        logger.info("SEMANTIC LAYER DEPLOYMENT STARTED")
        logger.info("=" * 60)

        # -----------------------------------------------------------------
        # Validate Registry
        # -----------------------------------------------------------------

        self.registry.validate()

        # -----------------------------------------------------------------
        # Execute SQL Scripts
        # -----------------------------------------------------------------

        execution_results = self.executor.execute_many(

            [script.path for script in self.registry]

        )

        # -----------------------------------------------------------------
        # Validate Deployment
        # -----------------------------------------------------------------

        validation = self.validator.validate()

        success = validation.passed

        # Cache deployment state

        self._is_deployed = success

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
    # Public API
    # -------------------------------------------------------------------------

    def deploy(self) -> SemanticDeploymentResult:
        """
        Deploy the Semantic Layer.
        """

        return self._deploy()

    # -------------------------------------------------------------------------

    def rebuild(self) -> SemanticDeploymentResult:
        """
        Backward-compatible alias for deploy().
        """

        logger.warning(

            "SemanticManager.rebuild() is deprecated. "
            "Use deploy() instead."

        )

        return self.deploy()

    # -------------------------------------------------------------------------

    def refresh(self) -> SemanticDeploymentResult:
        """
        Refresh the Semantic Layer.

        Current implementation performs a complete deployment.
        """

        logger.info("Refreshing Semantic Layer...")

        return self.deploy()

    # -------------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Validate the Semantic Layer.

        Validation always executes against the database.
        """

        return self.validator.validate()

    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return Semantic Layer status.

        Performs a one-time validation if the deployment state
        has not yet been established.
        """

        if not self._is_deployed:

            try:

                validation = self.validator.validate()

                self._is_deployed = validation.passed

            except Exception:

                self._is_deployed = False

        return "READY" if self._is_deployed else "NOT DEPLOYED"

    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Return framework version.
        """

        return "2.3.0"