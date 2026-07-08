"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : report.py
Package     : src.presentation
Purpose     : Enterprise Report Builder
Author      : ERIP
Version     : 3.0.0

Description
-----------
Enterprise report builder for the Presentation Framework.

The Report class provides a reusable mechanism for constructing
professional operational reports across all ERIP frameworks.

Responsibilities
----------------
- Assemble report sections
- Build complete reports
- Display reports
- Support fluent report construction

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Self

from .console import Console


# =============================================================================
# Report Section
# =============================================================================


@dataclass(slots=True, frozen=True)
class ReportSection:
    """
    Immutable report section.
    """

    title: str

    body: str


# =============================================================================
# Enterprise Report
# =============================================================================


class Report:
    """
    Enterprise Report Builder.

    Composes operational reports from reusable sections.
    """

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __init__(
        self,
        title: str,
    ) -> None:
        """
        Construct a report.

        Parameters
        ----------
        title
            Report title.
        """

        self._title = title

        self._sections: list[ReportSection] = []

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}"
            f"(title={self.title!r}, "
            f"sections={len(self)})"
        )

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def title(self) -> str:
        """
        Report title.
        """

        return self._title

    @property
    def sections(self) -> tuple[ReportSection, ...]:
        """
        Immutable report sections.
        """

        return tuple(self._sections)

    # -------------------------------------------------------------------------
    # Collection Protocol
    # -------------------------------------------------------------------------

    def __iter__(self) -> Iterator[ReportSection]:
        """
        Iterate over report sections.
        """

        return iter(self._sections)

    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        """
        Number of report sections.
        """

        return len(self._sections)

    # -------------------------------------------------------------------------

    def __bool__(self) -> bool:
        """
        Return True when the report contains sections.
        """

        return bool(self._sections)

    # -------------------------------------------------------------------------
    # Builder API
    # -------------------------------------------------------------------------

    def add_section(
        self,
        *,
        title: str,
        body: str,
    ) -> Self:
        """
        Add a report section.

        Returns
        -------
        Self
            Report instance for fluent chaining.
        """

        self._sections.append(

            ReportSection(

                title=title,

                body=body,

            )

        )

        return self

    # -------------------------------------------------------------------------

    def clear(self) -> Self:
        """
        Remove all report sections.

        Returns
        -------
        Self
            Report instance.
        """

        self._sections.clear()

        return self

    # -------------------------------------------------------------------------
    # Rendering
    # -------------------------------------------------------------------------

    def build(self) -> str:
        """
        Build the complete report.
        """

        lines: list[str] = [

            Console.header(

                self.title

            )

        ]

        for section in self:

            lines.extend(

                (

                    Console.section(

                        section.title

                    ),

                    section.body,

                )

            )

        lines.append(

            Console.footer()

        )

        return Console.join(

            *lines

        )

    # -------------------------------------------------------------------------

    def render(self) -> str:
        """
        Alias for build().
        """

        return self.build()

    # -------------------------------------------------------------------------

    def display(self) -> Self:
        """
        Display the report.

        Returns
        -------
        Self
            Report instance.
        """

        Console.display(

            self.build()

        )

        return self