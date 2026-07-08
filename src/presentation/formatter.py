"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : formatter.py
Package     : src.presentation
Purpose     : Enterprise Presentation Formatter
Author      : ERIP
Version     : 1.0.0

Description
-----------
Shared formatting utilities for Enterprise Presentation.

Responsibilities
----------------
- Numbers
- Percentages
- Durations
- Dates
- Memory
- Rows
- Boolean values

===============================================================================
"""

from __future__ import annotations

from datetime import datetime


# =============================================================================
# Formatter
# =============================================================================


class Formatter:
    """
    Enterprise presentation formatter.
    """

    # -------------------------------------------------------------------------
    # Numbers
    # -------------------------------------------------------------------------

    @staticmethod
    def number(value: int | float | None) -> str:
        """
        Format a numeric value.
        """

        if value is None:

            return "N/A"

        if isinstance(value, int):

            return f"{value:,}"

        return f"{value:,.2f}"

    # -------------------------------------------------------------------------
    # Rows
    # -------------------------------------------------------------------------

    @staticmethod
    def rows(value: int | None) -> str:
        """
        Format processed rows.
        """

        if value is None:

            return "N/A"

        return f"{value:,}"

    # -------------------------------------------------------------------------
    # Percentage
    # -------------------------------------------------------------------------

    @staticmethod
    def percent(value: float | None) -> str:
        """
        Format percentage.
        """

        if value is None:

            return "N/A"

        return f"{value:.2f}%"

    # -------------------------------------------------------------------------
    # Duration
    # -------------------------------------------------------------------------

    @staticmethod
    def duration(seconds: float | None) -> str:
        """
        Format execution duration.
        """

        if seconds is None:

            return "N/A"

        if seconds < 1:

            return f"{seconds * 1000:.2f} ms"

        return f"{seconds:.2f} sec"

    # -------------------------------------------------------------------------
    # Memory
    # -------------------------------------------------------------------------

    @staticmethod
    def memory(value: float | None) -> str:
        """
        Format memory usage.
        """

        if value is None:

            return "N/A"

        return f"{value:.2f} MB"

    # -------------------------------------------------------------------------
    # DateTime
    # -------------------------------------------------------------------------

    @staticmethod
    def datetime(value: datetime | None) -> str:
        """
        Format datetime.
        """

        if value is None:

            return "N/A"

        return value.strftime("%Y-%m-%d %H:%M:%S UTC")

    # -------------------------------------------------------------------------
    # Boolean
    # -------------------------------------------------------------------------

    @staticmethod
    def boolean(value: bool) -> str:
        """
        Format boolean.
        """

        return "YES" if value else "NO"

    # -------------------------------------------------------------------------
    # Text
    # -------------------------------------------------------------------------

    @staticmethod
    def text(value: str | None) -> str:
        """
        Format text values.
        """

        return value if value else "N/A"