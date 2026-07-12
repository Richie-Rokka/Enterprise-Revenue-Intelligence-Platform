"""
===============================================================================
Enterprise Order Payments Loader.

Responsibilities
----------------
• Load validated Order Payments data into staging.order_payments
• Execute PostgreSQL COPY
• Manage database transactions
• Return LoadResult

This loader represents the canonical "Load" stage for
the Order Payments ETL pipeline.
===============================================================================

Module      : load_order_payments.py
Package     : src.etl.load
Purpose     : Load Order Payments Data into staging.order_payments
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader


class OrderPaymentsLoader(BaseLoader):
    """
    Enterprise Order Payments Loader.
    """

    def __init__(
        self,
        context: ETLContext | None = None,
    ) -> None:

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

            context=context,

        )
