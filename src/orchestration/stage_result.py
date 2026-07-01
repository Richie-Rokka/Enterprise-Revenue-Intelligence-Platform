"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : stage_result.py
Package     : src.orchestration
Purpose     : Standard execution result returned by every platform stage
Author      : ERIP
Version     : 2.0.0

Description
-----------
Provides a standardized execution result for every stage executed by the
Enterprise Platform Engine.

Responsibilities
----------------
- Execution status
- Row metrics
- Runtime
- Warnings
- Errors
- Additional metadata

Notes
-----
Every pipeline stage must return a StageResult object.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# =============================================================================
# Stage Status
# =============================================================================

class StageStatus(str, Enum):
    """
    Supported execution states for a pipeline stage.
    """

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


# =============================================================================
# Stage Result
# =============================================================================

@dataclass(slots=True)
class StageResult:
    """
    Standard execution result returned by every pipeline stage.
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    stage_name: str

    status: StageStatus

    # -------------------------------------------------------------------------
    # Metrics
    # -------------------------------------------------------------------------

    rows_processed: int = 0
    rows_loaded: int = 0

    execution_seconds: float = 0.0

    warnings: int = 0
    errors: int = 0

    # -------------------------------------------------------------------------
    # Timing
    # -------------------------------------------------------------------------

    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    completed_at: datetime | None = None

    # -------------------------------------------------------------------------
    # Messaging
    # -------------------------------------------------------------------------

    message: str = ""

    # -------------------------------------------------------------------------
    # Extensibility
    # -------------------------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def complete(self) -> None:
        """
        Mark stage execution as complete.
        """

        self.completed_at = datetime.now(timezone.utc)

        self.execution_seconds = (
            self.completed_at - self.started_at
        ).total_seconds()

    def add_metadata(
        self,
        key: str,
        value: Any
    ) -> None:
        """
        Store execution metadata.
        """

        self.metadata[key] = value

    @property
    def succeeded(self) -> bool:
        """
        Returns True when the stage completed successfully.
        """

        return self.status == StageStatus.SUCCESS

    @property
    def failed(self) -> bool:
        """
        Returns True when the stage failed.
        """

        return self.status == StageStatus.FAILED

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the result into a dictionary.
        """

        return {
            "stage_name": self.stage_name,
            "status": self.status.value,
            "rows_processed": self.rows_processed,
            "rows_loaded": self.rows_loaded,
            "execution_seconds": self.execution_seconds,
            "warnings": self.warnings,
            "errors": self.errors,
            "message": self.message,
            "started_at": self.started_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat()
                if self.completed_at
                else None
            ),
            "metadata": self.metadata,
        }