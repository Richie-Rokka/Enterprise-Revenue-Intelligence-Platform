"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : base_extractor.py
Package     : src.etl.extract
Purpose     : Abstract Base Extractor
Author      : ERIP
Version     : 3.0.0

Description
-----------
Defines the enterprise interface implemented by every data extractor.

Responsibilities
----------------
• Read source data
• Return standardized DataFrame
• Update ETL Context
• Support future data sources

Supported Sources
-----------------
• CSV
• PostgreSQL
• SQL Server
• Snowflake
• BigQuery
• Excel
• REST API
• Parquet
• Future connectors

===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd

from src.etl.context import ETLContext


class BaseExtractor(ABC):
    """
    Enterprise abstract extractor.

    Every extractor must implement
    the extract() method.
    """

    # -------------------------------------------------------------------------

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        self.context = context

    # -------------------------------------------------------------------------

    @abstractmethod
    def extract(
        self,
    ) -> pd.DataFrame:
        """
        Extract data from the source.

        Returns
        -------
        pandas.DataFrame
            Raw extracted dataset.
        """

        raise NotImplementedError