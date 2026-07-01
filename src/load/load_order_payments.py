"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_order_payments.py
Package     : src.load
Purpose     : Load Order Payments Data into staging.order_payments
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class OrderPaymentsLoader(BaseLoader):
    """Enterprise Order Payments Loader."""

    def __init__(self) -> None:

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
        )


def main() -> None:

    OrderPaymentsLoader().run()


if __name__ == "__main__":
    main()