"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_seller.py
Package     : src.etl.load
Purpose     : Load Seller Data into staging.seller
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.seller_transformer import (
    SellerTransformer,
)


class SellerLoader(BaseLoader):
    """
    Enterprise Seller Loader.
    """

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

        self.context = ETLContext(

            pipeline_name="Seller Pipeline",

            source_name="Olist Sellers",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="seller",

        )

        self.transformer = SellerTransformer(

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
        Execute seller business transformations.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    SellerLoader().run()


if __name__ == "__main__":

    main()