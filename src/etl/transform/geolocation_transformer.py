"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : geolocation_transformer.py
Package     : src.etl.transform
Purpose     : Enterprise Geolocation Transformer
Author      : ERIP
Version     : 3.2.0
===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.transform.base_transformer import BaseTransformer
from src.observability import get_logger


logger = get_logger(__name__)


class GeolocationTransformer(BaseTransformer):
    """
    Enterprise Geolocation Transformer.
    """

    REQUIRED_COLUMNS = {

        "geolocation_zip_code_prefix",

        "geolocation_lat",

        "geolocation_lng",

        "geolocation_city",

        "geolocation_state",

    }

    NUMERIC_COLUMNS = [

        "geolocation_zip_code_prefix",

    ]

    FLOAT_COLUMNS = [

        "geolocation_lat",

        "geolocation_lng",

    ]

    # -----------------------------------------------------------------

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        super().__init__(context)

    # -----------------------------------------------------------------

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        logger.info(
            "Starting Geolocation transformation..."
        )

        dataframe = dataframe.copy()

        dataframe = self._standardize_columns(dataframe)

        self._validate_required_columns(dataframe)

        dataframe = self._normalize_location(dataframe)

        dataframe = self._convert_numeric_columns(dataframe)

        dataframe = self._convert_float_columns(dataframe)

        before = len(dataframe)

        dataframe = dataframe.drop_duplicates()

        duplicates_removed = before - len(dataframe)

        dataframe = dataframe.sort_values(

            by=[

                "geolocation_zip_code_prefix",

                "geolocation_city",

            ],

            kind="stable",

        ).reset_index(drop=True)

        self.context.add_rows_transformed(

            len(dataframe)

        )

        self.context.add_metadata(

            "duplicates_removed",

            duplicates_removed,

        )

        logger.info(

            "Geolocation transformation completed "

            "(%s rows, %s duplicates removed)",

            len(dataframe),

            duplicates_removed,

        )

        return dataframe

    # =================================================================

    def _standardize_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe.columns = (

            dataframe.columns

            .str.strip()

            .str.lower()

        )

        return dataframe

    # -----------------------------------------------------------------

    def _validate_required_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        missing = (

            self.REQUIRED_COLUMNS

            - set(dataframe.columns)

        )

        if missing:

            raise ValueError(

                f"Missing required columns: {sorted(missing)}"

            )

    # -----------------------------------------------------------------

    def _normalize_location(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["geolocation_city"] = (

            dataframe["geolocation_city"]

            .fillna("Unknown")

            .astype(str)

            .str.strip()

            .str.title()

        )

        dataframe["geolocation_state"] = (

            dataframe["geolocation_state"]

            .fillna("")

            .astype(str)

            .str.strip()

            .str.upper()

        )

        return dataframe

    # -----------------------------------------------------------------

    def _convert_numeric_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.NUMERIC_COLUMNS:

            dataframe[column] = (

                pd.to_numeric(

                    dataframe[column],

                    errors="coerce",

                )

                .astype("Int64")

            )

        return dataframe

    # -----------------------------------------------------------------

    def _convert_float_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.FLOAT_COLUMNS:

            dataframe[column] = pd.to_numeric(

                dataframe[column],

                errors="coerce",

            )

        return dataframe