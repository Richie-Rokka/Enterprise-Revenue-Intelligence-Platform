"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_order_items.py
Package     : src.load
Purpose     : Load Order Items Data into staging.order_items
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class OrderItemsLoader(BaseLoader):
    """Enterprise Order Items Loader."""

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


def main() -> None:

    OrderItemsLoader().run()


if __name__ == "__main__":
    main()