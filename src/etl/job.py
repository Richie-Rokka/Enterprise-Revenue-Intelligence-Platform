"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : job.py
Package     : src.etl
Purpose     : ETL Job Definition
Author      : ERIP
Version     : 3.0.0

Description
-----------
Defines an executable ETL job.

An ETL Job combines:

    • Dataset definition
    • Source configuration
    • Target configuration
    • Runtime configuration

Jobs are executed by the ETL Manager.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ETLJob:
    """
    Enterprise ETL Job.
    """

    # ---------------------------------------------------------------------
    # Identity
    # ---------------------------------------------------------------------

    name: str

    dataset: str

    # ---------------------------------------------------------------------
    # Source
    # ---------------------------------------------------------------------

    source_type: str

    source_path: Path | None = None

    source_options: dict[str, Any] = field(
        default_factory=dict
    )

    # ---------------------------------------------------------------------
    # Target
    # ---------------------------------------------------------------------

    target_schema: str = "staging"

    target_table: str = ""

    # ---------------------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------------------

    batch_size: int = 10000

    truncate_before_load: bool = False

    continue_on_error: bool = False

    enabled: bool = True