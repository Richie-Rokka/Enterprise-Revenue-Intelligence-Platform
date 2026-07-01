"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_product.py
Package     : src.load
Purpose     : Load Product Data into staging.product
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class ProductLoader(BaseLoader):
    """Enterprise Product Loader."""

    def __init__(self) -> None:

        super().__init__(
            source_file="data/raw/olist_products_dataset.csv",
            target_table="staging.product",
            required_columns=[
                "product_id",
                "product_category_name",
            ],
        )


def main() -> None:

    ProductLoader().run()


if __name__ == "__main__":
    main()