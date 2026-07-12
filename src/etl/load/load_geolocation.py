"""
===============================================================================
Enterprise Geolocation Loader.

Responsibilities
----------------
• Load validated Geolocation data into staging.geolocation
• Execute PostgreSQL COPY
• Manage database transactions
• Return LoadResult

This loader represents the canonical "Load" stage for
the Geolocation ETL pipeline.
===============================================================================

Module      : load_geolocation.py
Package     : src.etl.load
Purpose     : Load Geolocation Data into staging.geolocation
Author      : ERIP
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

from src.etl.context import ETLContext
from src.etl.load.base_loader import BaseLoader



class GeolocationLoader(BaseLoader):
    """
    Enterprise Geolocation Loader.
    """

    def __init__(
        self,
        context: ETLContext | None = None,
    ) -> None:

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

            context=context,

        )
