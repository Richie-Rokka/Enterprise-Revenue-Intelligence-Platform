"""
===============================================================================
Enterprise Product Loader.

Responsibilities
----------------
• Load validated Product data into staging.product
• Execute PostgreSQL COPY
• Manage database transactions
• Return LoadResult

This loader represents the canonical "Load" stage for
the Product ETL pipeline.
===============================================================================

Module      : load_product.py
Package     : src.etl.load
Purpose     : Load Product Data into staging.product
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader



class ProductLoader(BaseLoader):
    """
    Enterprise Product Loader.
    """

    def __init__(
        self,
        context: ETLContext | None = None,
    ) -> None:

        super().__init__(

            source_file="data/raw/olist_products_dataset.csv",

            target_table="staging.product",

            required_columns=[

                "product_id",

                "product_category_name",

            ],

            context=context,

        )
    