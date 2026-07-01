"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : stage.py
Package     : src.orchestration
Purpose     : Base class for all platform pipeline stages
Author      : ERIP
Version     : 2.0.0

Description
-----------
Defines the common interface that every pipeline stage must implement.

Responsibilities
----------------
- Stage identity
- Stage description
- Stage execution
- Validation
- Cleanup

Notes
-----
Every executable platform stage must inherit from Stage.

===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.orchestration.execution_context import ExecutionContext
from src.orchestration.stage_result import StageResult


class Stage(ABC):
    """
    Base class for all ERIP pipeline stages.
    """

    # -------------------------------------------------------------------------
    # Stage Metadata
    # -------------------------------------------------------------------------

    name: str = "Unnamed Stage"

    description: str = ""

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    def before_execute(
        self,
        context: ExecutionContext
    ) -> None:
        """
        Hook executed before the stage begins.

        Default implementation updates the current stage
        in the execution context.
        """

        context.set_stage(self.name)

    @abstractmethod
    def execute(
        self,
        context: ExecutionContext
    ) -> StageResult:
        """
        Execute the stage.

        Every stage must implement this method.
        """

        raise NotImplementedError

    def after_execute(
        self,
        context: ExecutionContext,
        result: StageResult
    ) -> None:
        """
        Hook executed after successful completion.

        Subclasses may override if additional
        post-processing is required.
        """

        return

    def validate(
        self,
        context: ExecutionContext
    ) -> bool:
        """
        Validate that the stage is ready to execute.

        Override when stage-specific validation
        is required.
        """

        return True

    def cleanup(
        self,
        context: ExecutionContext
    ) -> None:
        """
        Cleanup temporary resources.

        Override if the stage creates temporary
        files, tables or connections.
        """

        return

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}')"
        )