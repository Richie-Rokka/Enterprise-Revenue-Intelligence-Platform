"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_order_payments.py
Package     : src.etl.load
Purpose     : Load Order Payments Data into staging.order_payments
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.payment_transformer import (
    PaymentTransformer,
)


class OrderPaymentsLoader(BaseLoader):
    """
    Enterprise Order Payments Loader.
    """

    def __init__(self) -> None:

        super().__init__(

            source_file="data/raw/olist_order_payments_dataset.csv",

            target_table="staging.order_payments",

            required_columns=[

                "order_id",

                "payment_sequential",

                "payment_type",

                "payment_installments",

                "payment_value",

            ],

        )

        self.context = ETLContext(

            pipeline_name="Order Payments Pipeline",

            source_name="Olist Order Payments",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="order_payments",

        )

        self.transformer = PaymentTransformer(

            self.context

        )

    # -----------------------------------------------------------------

    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Dataset-specific cleaning.

        Uses the BaseLoader implementation.
        """

        return super().clean(

            dataframe

        )

    # -----------------------------------------------------------------

    def before_load(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute payment business transformations.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    OrderPaymentsLoader().run()


if __name__ == "__main__":

    main()