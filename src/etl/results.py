"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : results.py
Package     : src.etl
Purpose     : Enterprise ETL Result Models
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class LoadResult:
    """
    Enterprise Loader execution result.
    """

    target_table: str

    rows_loaded: int

    rows_rejected: int

    batch_id: UUID

    load_id: UUID

    duration_seconds: float

    success: bool

@dataclass(slots=True, frozen=True)
class PipelineResult:
    """
    Enterprise pipeline execution result.
    """

    pipeline_name: str

    rows_extracted: int

    rows_transformed: int

    rows_validated: int

    load_result: LoadResult