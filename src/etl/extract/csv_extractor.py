"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : csv_extractor.py
Package     : src.etl.extract
Purpose     : Generic CSV Extractor
Author      : ERIP
Version     : 3.0.0

Description
-----------
Enterprise CSV extractor implementation.

Supports:
    • UTF-8 CSV files
    • Configurable delimiter
    • Configurable encoding
    • Missing value handling
    • ETL Context integration

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.etl.context import ETLContext
from src.etl.extract.base_extractor import BaseExtractor
from src.observability import get_logger


logger = get_logger(__name__)


class CSVExtractor(BaseExtractor):
    """
    Generic CSV extractor.
    """

    # -------------------------------------------------------------------------

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        super().__init__(context)

    # -------------------------------------------------------------------------

    def extract(self) -> pd.DataFrame:
        """
        Extract a CSV dataset.

        Returns
        -------
        pandas.DataFrame
        """

        if self.context.source_path is None:

            raise ValueError(
                "ETLContext.source_path is not defined."
            )

        csv_path = Path(self.context.source_path)

        logger.info(
            "Extracting CSV dataset: %s",
            csv_path.name,
        )

        dataframe = pd.read_csv(

            csv_path,

            encoding="utf-8",

            low_memory=False,
        
        )

        self.context.add_rows_extracted(

            len(dataframe)

        )

        logger.info(

            "Extracted %s rows from %s",

            f"{len(dataframe):,}",

            self.context.source_path.name

        )

        return dataframe