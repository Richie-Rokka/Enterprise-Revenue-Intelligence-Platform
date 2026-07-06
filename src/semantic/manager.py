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

    def __init__(
        self,
        *,
        registry: SemanticRegistry,
        validator: SemanticValidator,
        executor: DatabaseExecutor,
    ) -> None:
        """
        Construct the Semantic Manager.

        Parameters
        ----------
        registry
            Shared Semantic Registry.

        validator
            Shared Semantic Validator.

        executor
            Shared SQL execution service.
        """

        self.registry = registry

        self.validator = validator

        self.executor = executor

        # ---------------------------------------------------------------------
        # Runtime State
        # ---------------------------------------------------------------------

        self._validation_result: ValidationResult | None = None

        self._validation_dirty: bool = True

    
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

        # Deployment changed the semantic layer.

        self._validation_dirty = True

        validation = self.validate()

        success = validation.passed

        # Cache deployment state

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
        self._validation_dirty = True
        
        return self._deploy()

    # -------------------------------------------------------------------------

    def rebuild(self) -> SemanticDeploymentResult:
        """
        Backward-compatible alias for deploy().
        """

        # ---------------------------------------------------------------------
        # Invalidate cached validation.
        # ---------------------------------------------------------------------
        
        self._validation_dirty = True
        

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

        self._validation_dirty = True

        logger.info("Refreshing Semantic Layer...")

        return self.deploy()

    # -------------------------------------------------------------------------

    def validate(self) -> ValidationResult:

        if self._validation_dirty:

            self._validation_result = self.validator.validate()

            self._validation_dirty = False

        return self._validation_result

    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return Semantic Layer status.
        """

        validation = self.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Return framework version.
        """

        return "2.3.0"