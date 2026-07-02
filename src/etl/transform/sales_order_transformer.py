"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : sales_order_transformer.py
Package     : src.etl.transform
Purpose     : Enterprise Sales Order Transformer
Author      : ERIP
Version     : 3.2.0

Description
-----------
Transforms raw sales order data into a standardized dataset suitable
for enterprise warehouse loading.

Responsibilities
----------------
• Validate required columns
• Standardize column names
• Normalize business values
• Convert timestamps
• Normalize string fields
• Remove duplicate orders
• Sort records
• Record transformation metrics

===============================================================================
"""

from __future__ import annotations

import pandas as pd

from src.etl.context import ETLContext
from src.etl.transform.base_transformer import BaseTransformer
from src.observability import get_logger


logger = get_logger(__name__)


class SalesOrderTransformer(BaseTransformer):
    """
    Enterprise Sales Order Transformer.
    """

    REQUIRED_COLUMNS = {

        "order_id",

        "customer_id",

        "order_status",

        "order_purchase_timestamp",

    }

    TIMESTAMP_COLUMNS = [

        "order_purchase_timestamp",

        "order_approved_at",

        "order_delivered_carrier_date",

        "order_delivered_customer_date",

        "order_estimated_delivery_date",

    ]

    STRING_COLUMNS = [

        "order_id",

        "customer_id",

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
        Apply enterprise business transformations.
        """

        logger.info(
            "Starting Sales Order transformation..."
        )

        dataframe = dataframe.copy()

        dataframe = self._standardize_columns(dataframe)

        self._validate_required_columns(dataframe)

        dataframe = self._normalize_order_status(dataframe)

        dataframe = self._normalize_strings(dataframe)

        dataframe = self._convert_timestamps(dataframe)

        dataframe, duplicates_removed = self._remove_duplicates(
            dataframe
        )

        dataframe = self._sort_orders(dataframe)

        dataframe = dataframe.reset_index(
            drop=True
        )

        # -------------------------------------------------------------
        # Update ETL Context
        # -------------------------------------------------------------

        self.context.add_rows_transformed(
            len(dataframe)
        )

        self.context.add_metadata(
            "duplicates_removed",
            duplicates_removed,
        )

        logger.info(

            "Sales Order transformation completed "

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

    def _normalize_order_status(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["order_status"] = (

            dataframe["order_status"]

            .fillna("unknown")

            .astype(str)

            .str.strip()

            .str.lower()

        )

        return dataframe

    # ---------------------------------------------------------------------

    def _normalize_strings(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.STRING_COLUMNS:

            dataframe[column] = (

                dataframe[column]

                .astype(str)

                .str.strip()

            )

        return dataframe

    # ---------------------------------------------------------------------

    def _convert_timestamps(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.TIMESTAMP_COLUMNS:

            dataframe[column] = pd.to_datetime(

                dataframe[column],

                errors="coerce",

            )

        dataframe = dataframe.dropna(

            subset=[

                "order_purchase_timestamp",

            ]

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

                "order_id",

            ],

            keep="first",

        )

        duplicates_removed = before - len(dataframe)

        return dataframe, duplicates_removed

    # ---------------------------------------------------------------------

    def _sort_orders(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe = dataframe.sort_values(

            by="order_purchase_timestamp",

            kind="stable",

        )

        return dataframe