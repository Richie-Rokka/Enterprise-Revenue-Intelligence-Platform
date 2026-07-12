"""
===============================================================================
Enterprise Seller Loader.

Responsibilities
----------------
• Load validated Seller data into staging.seller
• Execute PostgreSQL COPY
• Manage database transactions
• Return LoadResult

This loader represents the canonical "Load" stage for
the Seller ETL pipeline.
===============================================================================

Module      : load_seller.py
Package     : src.etl.load
Purpose     : Load Seller Data into staging.seller
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader



class SellerLoader(BaseLoader):
    """
    Enterprise Seller Loader.
    """

    def __init__(
        self,
        context: ETLContext | None = None,
    ) -> None:

        super().__init__(

            source_file="data/raw/olist_sellers_dataset.csv",

            target_table="staging.seller",

            required_columns=[

                "seller_id",

                "seller_zip_code_prefix",

                "seller_city",

                "seller_state",

            ],

            context=context,

        )
