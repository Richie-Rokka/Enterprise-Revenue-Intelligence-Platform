"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_order_reviews.py
Package     : src.load
Purpose     : Load Order Reviews Data into staging.order_reviews
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class OrderReviewsLoader(BaseLoader):
    """Enterprise Order Reviews Loader."""

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


def main() -> None:

    OrderReviewsLoader().run()


if __name__ == "__main__":
    main()