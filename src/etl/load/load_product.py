"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_product.py
Package     : src.etl.load
Purpose     : Load Product Data into staging.product
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.product_transformer import (
    ProductTransformer,
)


class ProductLoader(BaseLoader):
    """
    Enterprise Product Loader.
    """

    def __init__(self) -> None:

        super().__init__(

            source_file="data/raw/olist_products_dataset.csv",

            target_table="staging.product",

            required_columns=[

                "product_id",

                "product_category_name",

            ],

        )

        self.context = ETLContext(

            pipeline_name="Product Pipeline",

            source_name="Olist Products",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="product",

        )

        self.transformer = ProductTransformer(

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
        Execute product business transformations.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    ProductLoader().run()


if __name__ == "__main__":

    main()