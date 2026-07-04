"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : payment_transformer.py
Package     : src.etl.transform
Purpose     : Enterprise Payment Transformer
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


class PaymentTransformer(BaseTransformer):
    """
    Enterprise Payment Transformer.
    """

    REQUIRED_COLUMNS = {

        "order_id",

        "payment_sequential",

        "payment_type",

        "payment_installments",

        "payment_value",

    }

    ID_COLUMNS = [

        "order_id",

    ]

    INTEGER_COLUMNS = [

        "payment_sequential",

        "payment_installments",

    ]

    MONEY_COLUMNS = [

        "payment_value",

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

        logger.info(
            "Starting Payment transformation..."
        )

        dataframe = dataframe.copy()

        dataframe = self._standardize_columns(
            dataframe
        )

        self._validate_required_columns(
            dataframe
        )

        dataframe = self._normalize_ids(
            dataframe
        )

        dataframe = self._normalize_payment_type(
            dataframe
        )

        dataframe = self._convert_integer_columns(
            dataframe
        )

        dataframe = self._convert_money_columns(
            dataframe
        )

        dataframe, duplicates_removed = (
            self._remove_duplicates(
                dataframe
            )
        )

        dataframe = dataframe.sort_values(

            by=[

                "order_id",

                "payment_sequential",

            ],

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

            "Payment transformation completed "

            "(%s rows, %s duplicates removed)",

            len(dataframe),

            duplicates_removed,

        )

        return dataframe

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

    def _normalize_ids(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["order_id"] = (

            dataframe["order_id"]

            .fillna("")

            .astype(str)

            .str.strip()

        )

        return dataframe

    # ---------------------------------------------------------------------

    def _normalize_payment_type(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["payment_type"] = (

            dataframe["payment_type"]

            .fillna("unknown")

            .astype(str)

            .str.strip()

            .str.lower()

        )

        return dataframe

    # ---------------------------------------------------------------------

    def _convert_integer_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.INTEGER_COLUMNS:

            dataframe[column] = (

                pd.to_numeric(

                    dataframe[column],

                    errors="coerce",

                )

                .astype("Int64")

            )

        return dataframe

    # ---------------------------------------------------------------------

    def _convert_money_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.MONEY_COLUMNS:

            dataframe[column] = pd.to_numeric(

                dataframe[column],

                errors="coerce",

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

                "payment_sequential",

            ],

            keep="first",

        )

        duplicates_removed = before - len(dataframe)

        return dataframe, duplicates_removed