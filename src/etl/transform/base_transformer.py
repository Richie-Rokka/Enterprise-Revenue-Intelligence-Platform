"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : base_transformer.py
Package     : src.etl.transform
Purpose     : Abstract Base Transformer
Author      : ERIP
Version     : 3.0.0

Description
-----------
Defines the enterprise interface implemented by every transformer.

Responsibilities
----------------
• Clean raw data
• Standardize formats
• Apply business rules
• Return transformed DataFrame

===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd

from src.etl.context import ETLContext


class BaseTransformer(ABC):
    """
    Enterprise abstract transformer.

    Every transformer must implement
    the transform() method.
    """

    # -------------------------------------------------------------------------

    def __init__(
        self,
        context: ETLContext,
    ) -> None:

        self.context = context

    # -------------------------------------------------------------------------

    @abstractmethod
    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Transform the extracted dataset.

        Parameters
        ----------
        dataframe : pandas.DataFrame

        Returns
        -------
        pandas.DataFrame
        """

        raise NotImplementedError