"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : execution_context.py
Package     : src.orchestration
Purpose     : Shared execution context for the ERIP Platform Engine
Author      : ERIP
Version     : 2.0.0

Description
-----------
Provides a centralized execution context shared across every platform stage.

Responsibilities
----------------
- Pipeline metadata
- Database connection
- Configuration
- Logging
- Runtime state
- Execution metrics
- Shared metadata

Notes
-----
This class intentionally contains no business logic. It is a lightweight
container passed between orchestration stages.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class ExecutionContext:
    """
    Shared execution context for the Enterprise Platform Engine.
    """

    # -------------------------------------------------------------------------
    # Platform
    # -------------------------------------------------------------------------

    platform_name: str = "Enterprise Revenue Intelligence Platform"
    platform_version: str = "2.0.0"

    # -------------------------------------------------------------------------
    # Pipeline
    # -------------------------------------------------------------------------

    pipeline_name: str = "default_pipeline"
    environment: str = "development"
    run_id: str = field(default_factory=lambda: str(uuid4()))

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    start_time: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    current_stage: str = "Initialization"

    # -------------------------------------------------------------------------
    # Infrastructure
    # -------------------------------------------------------------------------

    engine: Any = None
    logger: Any = None
    config: Any = None

    # -------------------------------------------------------------------------
    # Metrics
    # -------------------------------------------------------------------------

    rows_processed: int = 0
    rows_loaded: int = 0

    warnings: int = 0
    errors: int = 0

    # -------------------------------------------------------------------------
    # Extensibility
    # -------------------------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def set_stage(self, stage_name: str) -> None:
        """
        Update the current pipeline stage.
        """
        self.current_stage = stage_name

    def add_rows_processed(self, count: int) -> None:
        """
        Increment processed row count.
        """
        self.rows_processed += count

    def add_rows_loaded(self, count: int) -> None:
        """
        Increment loaded row count.
        """
        self.rows_loaded += count

    def add_warning(self, count: int = 1) -> None:
        """
        Increment warning counter.
        """
        self.warnings += count

    def add_error(self, count: int = 1) -> None:
        """
        Increment error counter.
        """
        self.errors += count

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Store additional execution metadata.
        """
        self.metadata[key] = value

    @property
    def elapsed_seconds(self) -> float:
        """
        Return elapsed execution time in seconds.
        """
        return (
            datetime.now(timezone.utc) - self.start_time
        ).total_seconds()