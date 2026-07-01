"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_geolocation.py
Package     : src.load
Purpose     : Load Geolocation Data into staging.geolocation
Version     : 2.0.0
===============================================================================
"""

from src.load.base_loader import BaseLoader


class GeolocationLoader(BaseLoader):
    """Enterprise Geolocation Loader."""

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


def main() -> None:

    GeolocationLoader().run()


if __name__ == "__main__":
    main()