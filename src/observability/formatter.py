"""
Enterprise Revenue Intelligence Platform (ERIP)

Log Formatter

Provides standardized log formatting for all
platform loggers.
"""

import logging


class EnterpriseFormatter(logging.Formatter):
    """
    Enterprise log formatter.

    Format Example
    --------------
    2026-07-01 09:15:28 | INFO | build_fact_sales | Loading completed.
    """

    DEFAULT_FORMAT = (
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    )

    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(
        self,
        fmt=None,
        datefmt=None,
    ):
        """
        Initialize formatter.
        """

        super().__init__(
            fmt=fmt or self.DEFAULT_FORMAT,
            datefmt=datefmt or self.DEFAULT_DATE_FORMAT,
        )