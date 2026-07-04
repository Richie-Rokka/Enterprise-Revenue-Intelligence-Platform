"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : customer_transformer.py
Package     : src.etl.transform
Purpose     : Enterprise Customer Transformer
Author      : ERIP
Version     : 3.2.0

Description
-----------
Transforms raw customer data into a standardized dataset suitable
for enterprise warehouse loading.

Responsibilities
----------------
• Validate required columns
• Standardize column names
• Normalize customer identifiers
• Normalize geographic attributes
• Convert ZIP code datatype
• Remove duplicate customers
• Record transformation metrics

===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.transform.base_transformer import BaseTransformer
from src.observability import get_logger


logger = get_logger(__name__)


class CustomerTransformer(BaseTransformer):
    """
    Enterprise Customer Transformer.
    """

    REQUIRED_COLUMNS = {

        "customer_id",

        "customer_unique_id",

        "customer_zip_code_prefix",

        "customer_city",

        "customer_state",

    }

    ID_COLUMNS = [

        "customer_id",

        "customer_unique_id",

    ]

    # -------------------------------------------------------------------------

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        super().__init__(context)

    # -------------------------------------------------------------------------

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Apply enterprise customer transformations.
        """

        logger.info(
            "Starting Customer transformation..."
        )

        dataframe = dataframe.copy()

        dataframe = self._standardize_columns(
            dataframe
        )

        self._validate_required_columns(
            dataframe
        )

        dataframe = self._normalize_customer_ids(
            dataframe
        )

        dataframe = self._normalize_location(
            dataframe
        )

        dataframe = self._convert_zip_code(
            dataframe
        )

        dataframe, duplicates_removed = (
            self._remove_duplicates(
                dataframe
            )
        )

        dataframe = dataframe.sort_values(

            by="customer_id",

            kind="stable",

        ).reset_index(

            drop=True

        )

        self.context.add_rows_transformed(

            len(dataframe)

        )

        self.context.add_metadata(

            "duplicates_removed",

            duplicates_removed,

        )

        logger.info(

            "Customer transformation completed "

            "(%s rows, %s duplicates removed)",

            len(dataframe),

            duplicates_removed,

        )

        return dataframe

    # =====================================================================
    # Private Methods
    # =====================================================================

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

    # ---------------------------------------------------------------------

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

    # ---------------------------------------------------------------------

    def _normalize_customer_ids(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.ID_COLUMNS:

            dataframe[column] = (

                dataframe[column]

                .fillna("")

                .astype(str)

                .str.strip()

            )

        return dataframe

    # ---------------------------------------------------------------------

    def _normalize_location(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["customer_city"] = (

            dataframe["customer_city"]

            .fillna("Unknown")

            .astype(str)

            .str.strip()

            .str.title()

        )

        dataframe["customer_state"] = (

            dataframe["customer_state"]

            .fillna("")

            .astype(str)

            .str.strip()

            .str.upper()

        )

        return dataframe

    # ---------------------------------------------------------------------

    def _convert_zip_code(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["customer_zip_code_prefix"] = pd.to_numeric(

            dataframe["customer_zip_code_prefix"],

            errors="coerce",

        ).astype("Int64")

        return dataframe

    # ---------------------------------------------------------------------

    def _remove_duplicates(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[pd.DataFrame, int]:

        before = len(dataframe)

        dataframe = dataframe.drop_duplicates(

            subset=[

                "customer_id",

            ],

            keep="first",

        )

        duplicates_removed = before - len(dataframe)

        return dataframe, duplicates_removed