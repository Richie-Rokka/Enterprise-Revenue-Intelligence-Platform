"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_seller.py
Package     : src.load
Purpose     : Load Seller Data into staging.seller
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class SellerLoader(BaseLoader):
    """Enterprise Seller Loader."""

    def __init__(self) -> None:

        super().__init__(
            source_file="data/raw/olist_sellers_dataset.csv",
            target_table="staging.seller",
            required_columns=[
                "seller_id",
                "seller_zip_code_prefix",
                "seller_city",
                "seller_state",
            ],
        )


def main() -> None:

    SellerLoader().run()


if __name__ == "__main__":
    main()