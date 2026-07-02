"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_orders.py
Package     : src.etl.load
Purpose     : Load Orders Data into staging.orders
Author      : ERIP
Version     : 3.1.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.sales_order_transformer import (
    SalesOrderTransformer,
)


class OrdersLoader(BaseLoader):
    """
    Enterprise Orders Loader.
    """

    def __init__(self) -> None:

        super().__init__(

            source_file="data/raw/olist_orders_dataset.csv",

            target_table="staging.orders",

            required_columns=[

                "order_id",

                "customer_id",

                "order_status",

                "order_purchase_timestamp",

                "order_approved_at",

                "order_delivered_carrier_date",

                "order_delivered_customer_date",

                "order_estimated_delivery_date",

            ],

        )

        self.context = ETLContext(

            pipeline_name="Orders Pipeline",

            source_name="Olist Orders",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="orders",

        )

        self.transformer = SalesOrderTransformer(

            self.context

        )

    # ---------------------------------------------------------------------

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

    # ---------------------------------------------------------------------

    def before_load(

        self,

        dataframe: pd.DataFrame,

    ) -> pd.DataFrame:
        """
        Execute business transformations before loading.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    OrdersLoader().run()


if __name__ == "__main__":

    main()