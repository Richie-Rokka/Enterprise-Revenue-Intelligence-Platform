"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : console.py
Package     : src.presentation
Purpose     : Enterprise Console Formatting Service
Author      : ERIP
Version     : 2.0.0

Description
-----------
Shared console formatting service for the Enterprise Presentation
Framework.

The Console is responsible for constructing consistently formatted
presentation output across the Enterprise Revenue Intelligence Platform.

The Console DOES NOT print.

Instead, every method returns formatted text which can be displayed,
logged, emailed, written to disk, or returned from APIs.

Responsibilities
----------------
- Build framework headers
- Build section headers
- Build separators
- Build key/value rows
- Build status messages
- Build formatted reports

===============================================================================
"""

from __future__ import annotations

from . import theme


# =============================================================================
# Enterprise Console
# =============================================================================


class Console:
    """
    Enterprise Console Formatting Service.

    All methods return formatted strings.
    """

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------

    @classmethod
    def header(
        cls,
        title: str,
    ) -> str:
        """
        Build a framework header.
        """

        return "\n".join(
            (
                theme.BORDER * theme.WIDTH,
                title,
                theme.BORDER * theme.WIDTH,
            )
        )

    # -------------------------------------------------------------------------

    @classmethod
    def footer(cls) -> str:
        """
        Build a framework footer.
        """

        return theme.BORDER * theme.WIDTH

    # -------------------------------------------------------------------------

    @classmethod
    def section(
        cls,
        title: str,
    ) -> str:
        """
        Build a section header.
        """

        return "\n".join(
            (
                "",
                title,
                theme.SEPARATOR * theme.WIDTH,
            )
        )

    # -------------------------------------------------------------------------

    @classmethod
    def rule(cls) -> str:
        """
        Build a separator.
        """

        return theme.SEPARATOR * theme.WIDTH

    # -------------------------------------------------------------------------

    @classmethod
    def blank(cls) -> str:
        """
        Build a blank line.
        """

        return ""

    # -------------------------------------------------------------------------
    # Key / Value
    # -------------------------------------------------------------------------

    @classmethod
    def key_value(
        cls,
        key: str,
        value: object,
    ) -> str:
        """
        Build a formatted key/value pair.
        """

        return f"{key:<30}: {value}"


    # -------------------------------------------------------------------------

    @classmethod
    def key_values(
        cls,
        **values: object,
    ) -> str:
        """
        Build multiple key/value pairs.

        Parameters
        ----------
        **values
            Keyword/value pairs.

        Returns
        -------
        str
            Formatted key/value block.
        """

        return cls.join(

            *(
                cls.key_value(

                    key.replace("_", " ").title(),

                    value,

                )

                for key, value in values.items()

            )

        )

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    @classmethod
    def success(
        cls,
        message: str,
    ) -> str:
        """
        Build a success message.
        """

        return f"{theme.SUCCESS_SYMBOL} {message}"

    #-------------------------------------------------------------------------

    @classmethod
    def warning(
        cls,
        message: str,
    ) -> str:
        """
        Build a warning message.
        """

        return f"{theme.WARNING_SYMBOL} {message}"

    # -------------------------------------------------------------------------

    @classmethod
    def error(
        cls,
        message: str,
    ) -> str:
        """
        Build an error message.
        """

        return f"{theme.FAILURE_SYMBOL} {message}"

    # -------------------------------------------------------------------------

    @classmethod
    def info(
        cls,
        message: str,
    ) -> str:
        """
        Build an informational message.
        """

        return f"{theme.INFO_SYMBOL} {message}"

    # -------------------------------------------------------------------------
    # Report Helpers
    # -------------------------------------------------------------------------

    @classmethod
    def join(
        cls,
        *lines: str,
    ) -> str:
        """
        Join multiple formatted lines into a report.

        Empty or None values are ignored.
        """

        return "\n".join(

            line

            for line in lines

            if line

        )

    # -------------------------------------------------------------------------

    @classmethod
    def display(
        cls,
        report: str,
    ) -> None:
        """
        Display a formatted report.

        This is the only method that writes to stdout.
        """

        print(report)