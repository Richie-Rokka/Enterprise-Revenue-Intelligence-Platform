"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_customer.py
Package     : src.load
Purpose     : Load Customer Data into staging.customer
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class CustomerLoader(BaseLoader):
    """Enterprise Customer Loader."""

    def __init__(self) -> None:

        super().__init__(
            source_file="data/raw/olist_customers_dataset.csv",
            target_table="staging.customer",
            required_columns=[
                "customer_id",
                "customer_unique_id",
                "customer_zip_code_prefix",
                "customer_city",
                "customer_state",
            ],
        )


def main() -> None:

    CustomerLoader().run()


if __name__ == "__main__":
    main()