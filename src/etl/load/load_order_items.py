"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_order_items.py
Package     : src.etl.load
Purpose     : Load Order Items Data into staging.order_items
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.order_items_transformer import (
    OrderItemsTransformer,
)


class OrderItemsLoader(BaseLoader):
    """
    Enterprise Order Items Loader.
    """

    def __init__(self) -> None:

        super().__init__(

            source_file="data/raw/olist_order_items_dataset.csv",

            target_table="staging.order_items",

            required_columns=[

                "order_id",

                "order_item_id",

                "product_id",

                "seller_id",

                "shipping_limit_date",

                "price",

                "freight_value",

            ],

        )

        self.context = ETLContext(

            pipeline_name="Order Items Pipeline",

            source_name="Olist Order Items",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="order_items",

        )

        self.transformer = OrderItemsTransformer(

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
        Execute Order Items business transformations.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    OrderItemsLoader().run()


if __name__ == "__main__":

    main()