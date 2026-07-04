"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_order_reviews.py
Package     : src.etl.load
Purpose     : Load Order Reviews Data into staging.order_reviews
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.review_transformer import (
    ReviewTransformer,
)


class OrderReviewsLoader(BaseLoader):
    """
    Enterprise Order Reviews Loader.
    """

    def __init__(self) -> None:

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

        )

        self.context = ETLContext(

            pipeline_name="Order Reviews Pipeline",

            source_name="Olist Order Reviews",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="order_reviews",

        )

        self.transformer = ReviewTransformer(

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
        Execute review business transformations.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    OrderReviewsLoader().run()


if __name__ == "__main__":

    main()