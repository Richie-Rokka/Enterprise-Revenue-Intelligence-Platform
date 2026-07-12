"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : context.py
Package     : src.etl
Purpose     : Enterprise ETL Execution Context
Author      : ERIP
Version     : 3.2.0

Description
-----------
Provides shared runtime state for every ETL pipeline execution.

The ETLContext is shared across Extractors, Transformers,
Validators and Loaders.

Responsibilities
----------------
• Pipeline metadata
• Source metadata
• Target metadata
• Batch configuration
• Runtime metrics
• Execution statistics
• Shared objects
• Execution lifecycle
• Runtime messages

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


# =============================================================================
# ETL Context
# =============================================================================

@dataclass(slots=True)
class ETLContext:
    """
    Shared execution context for ETL pipelines.
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    pipeline_name: str

    run_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    # -------------------------------------------------------------------------
    # Source
    # -------------------------------------------------------------------------

    source_name: str = ""

    source_type: str = ""

    source_path: Path | None = None

    # -------------------------------------------------------------------------
    # Target
    # -------------------------------------------------------------------------

    target_schema: str = "analytics"

    target_table: str = ""

    # -------------------------------------------------------------------------
    # Runtime
    # -------------------------------------------------------------------------

    start_time: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    end_time: datetime | None = None

    status: str = "RUNNING"

    completed: bool = False

    batch_size: int = 10_000

    # -------------------------------------------------------------------------
    # Metrics
    # -------------------------------------------------------------------------

    rows_extracted: int = 0

    rows_transformed: int = 0

    rows_validated: int = 0

    rows_loaded: int = 0

    rows_failed: int = 0

    datasets_processed: int = 0

    # -------------------------------------------------------------------------
    # Runtime Messages
    # -------------------------------------------------------------------------

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    # -------------------------------------------------------------------------
    # Shared Objects
    # -------------------------------------------------------------------------

    engine: Any = None

    logger: Any = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    configuration: dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================================
    # Metrics
    # =========================================================================

    def add_rows_extracted(
        self,
        count: int
    ) -> None:

        self.rows_extracted += count

    # -------------------------------------------------------------------------

    def add_rows_transformed(
        self,
        count: int
    ) -> None:

        self.rows_transformed += count

    # -------------------------------------------------------------------------

    def add_rows_validated(
        self,
        count: int
    ) -> None:

        self.rows_validated += count

    # -------------------------------------------------------------------------

    def add_rows_loaded(
        self,
        count: int
    ) -> None:

        self.rows_loaded += count

    # -------------------------------------------------------------------------

    def add_rows_failed(
        self,
        count: int
    ) -> None:

        self.rows_failed += count

    def increment_datasets_processed(self) -> None:

        self.datasets_processed += 1

    # =========================================================================
    # Metadata
    # =========================================================================

    def add_metadata(
        self,
        key: str,
        value: Any
    ) -> None:

        self.metadata[key] = value

        return value

    # =========================================================================
    # Runtime Messages
    # =========================================================================

    def add_warning(
        self,
        message: str
    ) -> None:

        self.warnings.append(message)

    # -------------------------------------------------------------------------

    def add_error(
        self,
        message: str
    ) -> None:

        self.errors.append(message)

        self.status = "FAILED"

    # =========================================================================
    # Execution Lifecycle
    # =========================================================================

    def finish(self) -> None:
        """
        Mark the pipeline execution as complete.
        """

        self.end_time = datetime.now(
            timezone.utc
        )

        if self.status != "FAILED":

            self.status = "SUCCESS"

        self.completed = True

    # -------------------------------------------------------------------------

    def mark_failed(
        self,
        message: str
    ) -> None:
        """
        Mark the pipeline execution as failed.
        """

        self.add_error(message)

        self.end_time = datetime.now(
            timezone.utc
        )

        self.completed = True

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def elapsed_seconds(
        self
    ) -> float:
        """
        Backward-compatible execution timer.

        If the pipeline is still running,
        calculates the elapsed time from
        the start of execution.

        If the pipeline has completed,
        returns the total execution time.
        """

        end = self.end_time or datetime.now(
            timezone.utc
        )

        return (

            end

            - self.start_time

        ).total_seconds()

    # -------------------------------------------------------------------------

    @property
    def duration_seconds(
        self
    ) -> float:
        """
        Alias for elapsed_seconds.

        Preferred property for future code.
        """

        return self.elapsed_seconds