"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : execution.py
Package     : src.etl
Purpose     : ETL Execution Context
Author      : ERIP
Version     : 3.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class ETLExecution:
    """
    Runtime execution state for an ETL job.
    """

    execution_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    job_name: str = ""

    dataset: str = ""

    source_type: str = ""

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    finished_at: datetime | None = None

    status: str = "RUNNING"

    rows_extracted: int = 0

    rows_transformed: int = 0

    rows_validated: int = 0

    rows_loaded: int = 0

    rows_failed: int = 0

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    # ------------------------------------------------------------------

    def finish(self) -> None:

        self.finished_at = datetime.utcnow()

        if self.errors:

            self.status = "FAILED"

        else:

            self.status = "SUCCESS"