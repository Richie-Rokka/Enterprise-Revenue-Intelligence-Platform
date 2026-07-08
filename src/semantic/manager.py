"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : manager.py
Package     : src.semantic
Purpose     : Enterprise Semantic Layer Manager

Author      : ERIP

Version     : 3.0.0

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

Architecture
------------
Implements the Enterprise Template Method architecture established by
WarehouseManager while preserving Semantic Layer business logic.

===============================================================================
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from src.database.database_executor import (
    DatabaseExecutor,
    ExecutionResult,
)

from src.observability import get_logger

from src.runtime.manager import RuntimeManager
from src.runtime.models import FrameworkState

from .registry import SemanticRegistry
from .validator import (
    SemanticValidator,
    ValidationResult,
)

logger = get_logger(__name__)

T = TypeVar("T")


# =============================================================================
# Deployment Result
# =============================================================================


@dataclass(slots=True)
class SemanticDeploymentResult:
    """
    Overall Semantic Layer deployment result.
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

    Public façade for all Semantic Layer services.
    """

    VERSION = "3.0.0"

    FRAMEWORK = "Semantic"

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __init__(
        self,
        *,
        registry: SemanticRegistry,
        validator: SemanticValidator,
        executor: DatabaseExecutor,
        runtime: RuntimeManager,
    ) -> None:
        """
        Construct the Enterprise Semantic Manager.
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
        Execute a Semantic Layer operation under Runtime control.
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
    # Public API
    # -------------------------------------------------------------------------

    def deploy(self) -> SemanticDeploymentResult:
        """
        Deploy the Semantic Layer.
        """

        return self._execute_runtime_operation(

            operation="Deploy",

            state=FrameworkState.DEPLOYING,

            action=self._deploy,

        )

    # -------------------------------------------------------------------------

    def rebuild(self) -> SemanticDeploymentResult:
        """
        Build or rebuild the Semantic Layer.

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

        return self._execute_runtime_operation(

            operation="Refresh",

            state=FrameworkState.REFRESHING,

            action=self._refresh,

        )

    # -------------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Validate the Semantic Layer.

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

    def status(self) -> str:
        """
        Return Semantic Layer status.
        """

        validation = self.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------

    @classmethod
    def version(cls) -> str:
        """
        Return framework version.
        """

        return cls.VERSION
        # =========================================================================
    # Private Business Logic
    # =========================================================================

    # -------------------------------------------------------------------------
    # Deployment
    # -------------------------------------------------------------------------

    def _deploy(self) -> SemanticDeploymentResult:
        """
        Deploy the complete Semantic Layer.
        """

        self._validation_dirty = True

        logger.info("=" * 60)
        logger.info("SEMANTIC LAYER DEPLOYMENT STARTED")
        logger.info("=" * 60)

        # ---------------------------------------------------------------------
        # Validate Registry
        # ---------------------------------------------------------------------

        self.registry.validate()

        # ---------------------------------------------------------------------
        # Execute Semantic Scripts
        # ---------------------------------------------------------------------

        execution_results = self.executor.execute_many(

            [script.path for script in self.registry]

        )

        # ---------------------------------------------------------------------
        # Runtime Validation Phase
        # ---------------------------------------------------------------------

        self.runtime.state(

            FrameworkState.VALIDATING

        )

        validation = self.validate()

        success = validation.passed

        # ---------------------------------------------------------------------
        # Deployment Summary
        # ---------------------------------------------------------------------

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
    # Refresh
    # -------------------------------------------------------------------------

    def _refresh(self) -> SemanticDeploymentResult:
        """
        Refresh the Semantic Layer.

        Current implementation performs a complete deployment.
        """

        self._validation_dirty = True

        logger.info("Refreshing Semantic Layer...")

        return self._deploy()