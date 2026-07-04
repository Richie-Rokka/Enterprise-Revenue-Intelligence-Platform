"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_geolocation.py
Package     : src.etl.load
Purpose     : Load Geolocation Data into staging.geolocation
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader
from src.etl.transform.geolocation_transformer import (
    GeolocationTransformer,
)


class GeolocationLoader(BaseLoader):
    """
    Enterprise Geolocation Loader.
    """

    def __init__(self) -> None:

        super().__init__(

            source_file="data/raw/olist_geolocation_dataset.csv",

            target_table="staging.geolocation",

            required_columns=[

                "geolocation_zip_code_prefix",

                "geolocation_lat",

                "geolocation_lng",

                "geolocation_city",

                "geolocation_state",

            ],

            remove_duplicates=False,

        )

        self.context = ETLContext(

            pipeline_name="Geolocation Pipeline",

            source_name="Olist Geolocation",

            source_type="CSV",

            source_path=self.source_file,

            target_schema="staging",

            target_table="geolocation",

        )

        self.transformer = GeolocationTransformer(

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
        Execute geolocation business transformations.
        """

        return self.transformer.transform(

            dataframe

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def main() -> None:

    GeolocationLoader().run()


if __name__ == "__main__":

    main()