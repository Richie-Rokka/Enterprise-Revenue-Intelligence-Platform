"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : transformations.py
Package     : src.etl.transform
Purpose     : Shared Data Transformation Utilities
Author      : ERIP
Version     : 3.0.0

Description
-----------
Provides reusable transformation functions shared across every ETL
Transformer.

Responsibilities
----------------
• Standardize column names
• Remove duplicate records
• Trim whitespace
• Normalize null values
• Convert datetime columns
• Convert numeric columns
• Validate required columns

Notes
-----
These functions are intentionally stateless.

No function should know anything about a specific dataset.

===============================================================================
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


# =============================================================================
# Column Standardization
# =============================================================================

def standardize_column_names(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize DataFrame column names.
    """

    dataframe = dataframe.copy()

    dataframe.columns = (

        dataframe.columns

        .str.strip()

        .str.lower()

        .str.replace(" ", "_", regex=False)

        .str.replace("-", "_", regex=False)

    )

    return dataframe


# =============================================================================
# Duplicate Removal
# =============================================================================

def remove_duplicates(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """

    return dataframe.drop_duplicates().reset_index(drop=True)


# =============================================================================
# Trim String Columns
# =============================================================================

def trim_string_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove leading/trailing whitespace from object columns.
    """

    dataframe = dataframe.copy()

    object_columns = dataframe.select_dtypes(
        include="object"
    ).columns

    for column in object_columns:

        dataframe[column] = dataframe[column].str.strip()

    return dataframe


# =============================================================================
# Normalize Null Values
# =============================================================================

def normalize_null_values(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Normalize blank strings to NULL.
    """

    dataframe = dataframe.copy()

    dataframe = dataframe.replace(

        {

            "": pd.NA,

            " ": pd.NA,

        }

    )

    return dataframe


# =============================================================================
# Datetime Conversion
# =============================================================================

def convert_datetime_columns(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """
    Convert columns to datetime.
    """

    dataframe = dataframe.copy()

    for column in columns:

        if column in dataframe.columns:

            dataframe[column] = pd.to_datetime(

                dataframe[column],

                errors="coerce",

            )

    return dataframe


# =============================================================================
# Numeric Conversion
# =============================================================================

def convert_numeric_columns(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """
    Convert columns to numeric.
    """

    dataframe = dataframe.copy()

    for column in columns:

        if column in dataframe.columns:

            dataframe[column] = pd.to_numeric(

                dataframe[column],

                errors="coerce",

            )

    return dataframe


# =============================================================================
# Required Column Validation
# =============================================================================

def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: Iterable[str],
) -> None:
    """
    Validate required columns exist.
    """

    missing = sorted(

        set(required_columns)

        - set(dataframe.columns)

    )

    if missing:

        raise ValueError(

            "Missing required columns: "

            + ", ".join(missing)

        )