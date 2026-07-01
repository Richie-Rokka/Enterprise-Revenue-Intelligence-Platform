"""
validation.py
Enterprise Revenue Intelligence Platform

Reusable validation functions used across all ETL pipelines.
"""

import pandas as pd


# ==========================================================
# EMPTY DATAFRAME
# ==========================================================

def check_empty(
    dataframe: pd.DataFrame,
    table_name: str
) -> None:
    """
    Validate that a DataFrame is not empty.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame to validate.

    table_name : str
        Name of the table being validated.

    Raises
    ------
    ValueError
        If the DataFrame contains no rows.
    """

    if dataframe.empty:

        raise ValueError(
            f"Validation Failed: '{table_name}' is empty."
        )


# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

def check_required_columns(
    dataframe: pd.DataFrame,
    columns: list[str]
) -> None:
    """
    Validate that required columns contain no NULL values.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame to validate.

    columns : list[str]
        List of required columns.

    Raises
    ------
    ValueError
        If a required column is missing or contains NULL values.
    """

    for column in columns:

        # Check column exists

        if column not in dataframe.columns:

            raise ValueError(
                f"Validation Failed: Column '{column}' does not exist."
            )

        # Check for NULL values

        missing = dataframe[column].isnull().sum()

        if missing > 0:

            raise ValueError(
                f"Validation Failed: Column '{column}' "
                f"contains {missing:,} NULL value(s)."
            )