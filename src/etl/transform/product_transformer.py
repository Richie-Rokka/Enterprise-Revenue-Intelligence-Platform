"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : product_transformer.py
Package     : src.etl.transform
Purpose     : Enterprise Product Transformer
Author      : ERIP
Version     : 3.2.0

Description
-----------
Transforms raw product data into a standardized dataset suitable
for enterprise warehouse loading.

Responsibilities
----------------
• Validate required columns
• Standardize column names
• Normalize product identifiers
• Normalize product category
• Convert numeric attributes
• Remove duplicate products
• Record transformation metrics

===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.transform.base_transformer import BaseTransformer
from src.observability import get_logger


logger = get_logger(__name__)


class ProductTransformer(BaseTransformer):
    """
    Enterprise Product Transformer.
    """

    REQUIRED_COLUMNS = {

        "product_id",

        "product_category_name",

    }

    NUMERIC_COLUMNS = [

        "product_name_lenght",

        "product_description_lenght",

        "product_photos_qty",

        "product_weight_g",

        "product_length_cm",

        "product_height_cm",

        "product_width_cm",

    ]

    # ---------------------------------------------------------------------

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        super().__init__(context)

    # ---------------------------------------------------------------------

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Apply enterprise business transformations.
        """

        logger.info(
            "Starting Product transformation..."
        )

        dataframe = dataframe.copy()

        dataframe = self._standardize_columns(
            dataframe
        )

        self._validate_required_columns(
            dataframe
        )

        dataframe = self._normalize_product_id(
            dataframe
        )

        dataframe = self._normalize_category(
            dataframe
        )

        dataframe = self._convert_numeric_columns(
            dataframe
        )

        dataframe, duplicates_removed = (
            self._remove_duplicates(
                dataframe
            )
        )

        dataframe = dataframe.sort_values(

            by="product_id",

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

            "Product transformation completed "

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

    def _normalize_product_id(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["product_id"] = (

            dataframe["product_id"]

            .fillna("")

            .astype(str)

            .str.strip()

        )

        return dataframe

    # ---------------------------------------------------------------------

    def _normalize_category(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["product_category_name"] = (

            dataframe["product_category_name"]

            .fillna("unknown")

            .astype(str)

            .str.strip()

            .str.lower()

        )

        return dataframe

    # ---------------------------------------------------------------------

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

    # ---------------------------------------------------------------------

    def _remove_duplicates(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[pd.DataFrame, int]:

        before = len(dataframe)

        dataframe = dataframe.drop_duplicates(

            subset=[

                "product_id",

            ],

            keep="first",

        )

        duplicates_removed = (

            before

            - len(dataframe)

        )

        return (

            dataframe,

            duplicates_removed,

        )