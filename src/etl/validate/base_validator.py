"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : base_validator.py
Package     : src.etl.validate
Purpose     : Abstract Base Validator
Author      : ERIP
Version     : 3.0.0

Description
-----------
Defines the enterprise validation interface implemented by every ETL
validator.

Responsibilities
----------------
• Validate transformed datasets
• Enforce business rules
• Update ETL execution metrics
• Raise validation exceptions when required

Notes
-----
This module contains no dataset-specific validation logic.

Concrete validators should inherit from BaseValidator.

===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd

from src.etl.context import ETLContext


class BaseValidator(ABC):
    """
    Enterprise abstract validator.

    Every validator must implement the validate() method.
    """

    # -------------------------------------------------------------------------

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        self.context = context

    # -------------------------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate a transformed dataset.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataset to validate.

        Returns
        -------
        pandas.DataFrame
            Validated dataset.

        Raises
        ------
        ValueError
            If validation fails.
        """

        raise NotImplementedError