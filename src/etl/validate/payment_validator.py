"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : payment_validator.py
Package     : src.etl.validate
Purpose     : Enterprise Payment Validator
Author      : ERIP
Version     : 3.3.0

Description
-----------
Enterprise validator for the Order Payments dataset.

Responsibilities
----------------
• Validate transformed payment data
• Enforce payment business rules
• Update ETL execution metrics
• Return validated dataset

Dataset-specific business rules will be added incrementally.

===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.validate.base_validator import BaseValidator


class PaymentValidator(BaseValidator):
    """
    Enterprise Payment Validator.
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
        Validate the transformed payment dataset.
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
        # Future business rules:
        #
        # • Mandatory order_id
        # • Positive payment_value
        # • Positive payment_installments
        # • Valid payment_type
        # • Duplicate payment detection
        #
        # -----------------------------------------------------------------

        return dataframe