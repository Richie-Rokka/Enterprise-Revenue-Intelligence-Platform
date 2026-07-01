"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_orders.py
Package     : src.load
Purpose     : Load Orders Data into staging.orders
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class OrdersLoader(BaseLoader):
    """Enterprise Orders Loader."""

    def __init__(self) -> None:

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
        )


def main() -> None:

    OrdersLoader().run()


if __name__ == "__main__":
    main()