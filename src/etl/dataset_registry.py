"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : dataset_registry.py
Package     : src.etl
Purpose     : Dataset Registry
Author      : ERIP
Version     : 3.0.0

Description
-----------
Central registry that defines every dataset supported by ERIP.

Each dataset specifies:

    • Source type
    • Extractor
    • Transformer
    • Validator
    • Loader

This allows new datasets to be added without modifying the ETL engine.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from src.etl.extract.base_extractor import BaseExtractor
from src.etl.transform.base_transformer import BaseTransformer
from src.etl.validate.base_validator import BaseValidator
from src.etl.load.base_loader import BaseLoader


# =============================================================================
# Dataset Definition
# =============================================================================

@dataclass(slots=True)
class DatasetDefinition:
    """
    Enterprise dataset definition.
    """

    name: str

    source_type: str

    extractor: Type[BaseExtractor]

    transformer: Type[BaseTransformer]

    validator: Type[BaseValidator]

    loader: Type[BaseLoader]


# =============================================================================
# Dataset Registry
# =============================================================================

class DatasetRegistry:
    """
    Enterprise Dataset Registry.
    """

    _datasets: dict[str, DatasetDefinition] = {}

    # ---------------------------------------------------------------------

    @classmethod
    def register(
        cls,
        dataset: DatasetDefinition,
    ) -> None:

        cls._datasets[

            dataset.name.lower()

        ] = dataset

    # ---------------------------------------------------------------------

    @classmethod
    def get(
        cls,
        dataset_name: str,
    ) -> DatasetDefinition:

        dataset_name = dataset_name.lower()

        if dataset_name not in cls._datasets:

            raise KeyError(

                f"Dataset '{dataset_name}' is not registered."

            )

        return cls._datasets[dataset_name]

    # ---------------------------------------------------------------------

    @classmethod
    def exists(
        cls,
        dataset_name: str,
    ) -> bool:

        return (

            dataset_name.lower()

            in cls._datasets

        )

    # ---------------------------------------------------------------------

    @classmethod
    def registered_datasets(
        cls,
    ) -> list[str]:

        return sorted(

            cls._datasets.keys()

        )

    # ---------------------------------------------------------------------

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._datasets.clear()