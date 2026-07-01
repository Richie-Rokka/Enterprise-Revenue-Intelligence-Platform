"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_product_category_translation.py
Package     : src.load
Purpose     : Load Product Category Translation Data
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class ProductCategoryTranslationLoader(BaseLoader):
    """Enterprise Product Category Translation Loader."""

    def __init__(self) -> None:

        super().__init__(
            source_file="data/raw/product_category_name_translation.csv",
            target_table="staging.product_category_translation",
            required_columns=[
                "product_category_name",
                "product_category_name_english",
            ],
        )


def main() -> None:

    ProductCategoryTranslationLoader().run()


if __name__ == "__main__":
    main()