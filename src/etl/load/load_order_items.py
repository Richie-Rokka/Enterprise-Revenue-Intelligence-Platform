"""
===============================================================================
Enterprise Order Items Loader.

Responsibilities
----------------
• Load validated Order Items data into staging.order_items
• Execute PostgreSQL COPY
• Manage database transactions
• Return LoadResult

This loader represents the canonical "Load" stage for
the Order Items ETL pipeline.
===============================================================================

Module      : load_order_items.py
Package     : src.etl.load
Purpose     : Load Order Items Data into staging.order_items
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader



class OrderItemsLoader(BaseLoader):
    """
    Enterprise Order Items Loader.
    """

    def __init__(
        self,
        context: ETLContext | None = None,
    ) -> None:

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

            context=context,

        )
