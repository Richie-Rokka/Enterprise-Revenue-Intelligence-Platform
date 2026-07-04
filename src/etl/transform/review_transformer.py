"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : review_transformer.py
Package     : src.etl.transform
Purpose     : Enterprise Review Transformer
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


class ReviewTransformer(BaseTransformer):
    """
    Enterprise Review Transformer.
    """

    REQUIRED_COLUMNS = {

        "review_id",

        "order_id",

        "review_score",

        "review_creation_date",

        "review_answer_timestamp",

    }

    ID_COLUMNS = [

        "review_id",

        "order_id",

    ]

    COMMENT_COLUMNS = [

        "review_comment_title",

        "review_comment_message",

    ]

    DATETIME_COLUMNS = [

        "review_creation_date",

        "review_answer_timestamp",

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
            "Starting Review transformation..."
        )

        dataframe = dataframe.copy()

        dataframe = self._standardize_columns(dataframe)

        self._validate_required_columns(dataframe)

        dataframe = self._normalize_ids(dataframe)

        dataframe = self._normalize_comments(dataframe)

        dataframe = self._convert_review_score(dataframe)

        dataframe = self._convert_datetime_columns(dataframe)

        dataframe, duplicates_removed = self._remove_duplicates(
            dataframe
        )

        dataframe = dataframe.sort_values(

            by=[

                "review_creation_date",

                "review_id",

            ],

            kind="stable",

        ).reset_index(drop=True)

        self.context.add_rows_transformed(len(dataframe))

        self.context.add_metadata(

            "duplicates_removed",

            duplicates_removed,

        )

        logger.info(

            "Review transformation completed "

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

        for column in self.ID_COLUMNS:

            dataframe[column] = (

                dataframe[column]

                .fillna("")

                .astype(str)

                .str.strip()

            )

        return dataframe

    # ---------------------------------------------------------------------

    def _normalize_comments(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.COMMENT_COLUMNS:

            dataframe[column] = (

                dataframe[column]

                .fillna("")

                .astype(str)

                .str.strip()

            )

        return dataframe

    # ---------------------------------------------------------------------

    def _convert_review_score(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["review_score"] = (

            pd.to_numeric(

                dataframe["review_score"],

                errors="coerce",

            )

            .astype("Int64")

        )

        return dataframe

    # ---------------------------------------------------------------------

    def _convert_datetime_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.DATETIME_COLUMNS:

            dataframe[column] = pd.to_datetime(

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

            subset=["review_id"],

            keep="first",

        )

        duplicates_removed = before - len(dataframe)

        return dataframe, duplicates_removed