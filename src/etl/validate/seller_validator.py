"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : seller_validator.py
Package     : src.etl.validate
Purpose     : Enterprise Seller Validator
Author      : ERIP
Version     : 3.3.0

Description
-----------
Enterprise validator for the Seller dataset.

Responsibilities
----------------
• Validate transformed Seller data
• Enforce Seller business rules
• Update ETL execution metrics
• Return validated dataset

Dataset-specific business rules will be added incrementally.

===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.validate.base_validator import BaseValidator


class SellerValidator(BaseValidator):
    """
    Enterprise Seller Validator.
    """

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        super().__init__(context)

    # ---------------------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate the transformed Seller dataset.
        """

        # -----------------------------------------------------------------
        # Enterprise Metrics
        # -----------------------------------------------------------------

        self.context.add_rows_validated(
            len(dataframe)
        )

        # -----------------------------------------------------------------
        # Dataset-specific validation
        # -----------------------------------------------------------------
        #
        # Future Seller business rules:
        #
        # • Mandatory seller_id
        # • Valid seller_state
        # • Valid ZIP code
        # • Duplicate seller detection
        #
        # -----------------------------------------------------------------

        return dataframe