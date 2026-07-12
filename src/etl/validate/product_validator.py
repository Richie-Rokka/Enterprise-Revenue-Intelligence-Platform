"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : product_validator.py
Package     : src.etl.validate
Purpose     : Enterprise Product Validator
Author      : ERIP
Version     : 3.3.0

Description
-----------
Enterprise validator for the Product dataset.

Responsibilities
----------------
• Validate transformed Product data
• Enforce Product business rules
• Update ETL execution metrics
• Return validated dataset

Dataset-specific business rules will be added incrementally.

===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.validate.base_validator import BaseValidator


class ProductValidator(BaseValidator):
    """
    Enterprise Product Validator.
    """

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        super().__init__(context)

    # -------------------------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate the transformed Product dataset.
        """

        # ---------------------------------------------------------------------
        # Enterprise Metrics
        # ---------------------------------------------------------------------

        self.context.add_rows_validated(
            len(dataframe)
        )

        # ---------------------------------------------------------------------
        # Dataset-specific validation
        # ---------------------------------------------------------------------
        #
        # Future Product business rules:
        #
        # • Mandatory product_id
        # • Valid category name
        # • Positive dimensions
        # • Positive weight
        # • Duplicate product detection
        #
        # ---------------------------------------------------------------------

        return dataframe