"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_customer.py
Package     : src.etl.load
Purpose     : Load Customer Data into staging.customer
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.customer_transformer import (
    CustomerTransformer,
)


class CustomerLoader(BaseLoader):
    """
    Enterprise Customer Loader.
    """

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

        self.context = ETLContext(

            pipeline_name="Customer Pipeline",

            source_name="Olist Customers",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="customer",

        )

        self.transformer = CustomerTransformer(

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
        Execute customer business transformations.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    CustomerLoader().run()


if __name__ == "__main__":

    main()