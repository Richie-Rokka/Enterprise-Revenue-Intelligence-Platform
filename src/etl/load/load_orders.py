"""
===============================================================================

Enterprise Orders Loader.

Responsibilities
----------------
• Load validated Orders data into staging.orders
• Execute PostgreSQL COPY
• Manage database transactions
• Return LoadResult

This loader represents the canonical "Load" stage for
the Orders ETL pipeline.

===============================================================================

Module      : load_orders.py
Package     : src.etl.load
Purpose     : Load Orders Data into staging.orders
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader



class OrdersLoader(BaseLoader):
    """
    Enterprise Orders Loader.
    """

    def __init__(
        self,
        context: ETLContext | None = None,
    ) -> None:

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

            context=context,

        )
