"""
===============================================================================
Enterprise Order Reviews Loader.

Responsibilities
----------------
• Load validated Order Reviews data into staging.order_reviews
• Execute PostgreSQL COPY
• Manage database transactions
• Return LoadResult

This loader represents the canonical "Load" stage for
the Order Reviews ETL pipeline.
===============================================================================

Module      : load_order_reviews.py
Package     : src.etl.load
Purpose     : Load Order Reviews Data into staging.order_reviews
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader


class OrderReviewsLoader(BaseLoader):
    """
    Enterprise Order Reviews Loader.
    """

    def __init__(
        self,
        context: ETLContext | None = None,
    ) -> None:

        super().__init__(

            source_file="data/raw/olist_order_reviews_dataset.csv",

            target_table="staging.order_reviews",

            required_columns=[

                "review_id",

                "order_id",

                "review_score",

                "review_creation_date",

                "review_answer_timestamp",

            ],

            context=context,

        )
