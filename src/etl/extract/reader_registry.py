"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : reader_registry.py
Package     : src.etl.extract
Purpose     : Reader Registry
Author      : ERIP
Version     : 3.0.0

Description
-----------
Central registry for all supported data readers.

Responsibilities
----------------
• Register reader implementations
• Resolve reader by source type
• Validate supported source types

===============================================================================
"""

from __future__ import annotations

from typing import Type

from src.etl.context import ETLContext
from src.etl.extract.base_extractor import BaseExtractor


class ReaderRegistry:
    """
    Enterprise Reader Registry.
    """

    _registry: dict[str, Type[BaseExtractor]] = {}

    # ---------------------------------------------------------------------

    @classmethod
    def register(
        cls,
        source_type: str,
        reader: Type[BaseExtractor],
    ) -> None:
        """
        Register a reader.
        """

        cls._registry[source_type.lower()] = reader

    # ---------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        source_type: str,
        context: ETLContext,
    ) -> BaseExtractor:
        """
        Create a reader instance.
        """

        source_type = source_type.lower()

        if source_type not in cls._registry:

            supported = ", ".join(sorted(cls._registry))

            raise ValueError(
                f"Unsupported source type: '{source_type}'. "
                f"Supported: {supported}"
            )

        return cls._registry[source_type](context)

    # ---------------------------------------------------------------------

    @classmethod
    def supported_sources(cls) -> list[str]:
        """
        Return supported source types.
        """

        return sorted(cls._registry.keys())

    # ---------------------------------------------------------------------

    @classmethod
    def clear(cls) -> None:
        """
        Clear registry.
        """

        cls._registry.clear()