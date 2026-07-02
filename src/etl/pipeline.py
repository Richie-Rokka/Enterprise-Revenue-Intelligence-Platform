"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : pipeline.py
Package     : src.etl
Purpose     : Enterprise ETL Pipeline Definition
Author      : ERIP
Version     : 3.0.0

Description
-----------
Defines a complete ETL pipeline by composing the four ETL components:

    • Extractor
    • Transformer
    • Validator
    • Loader

The ETL Manager executes pipelines rather than individual components.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from src.etl.context import ETLContext
from src.etl.extract.base_extractor import BaseExtractor
from src.etl.transform.base_transformer import BaseTransformer
from src.etl.validate.base_validator import BaseValidator
from src.etl.load.base_loader import BaseLoader


@dataclass(slots=True)
class ETLPipeline:
    """
    Enterprise ETL Pipeline.

    Represents a complete ETL workflow for a single dataset.
    """

    name: str

    context: ETLContext

    extractor: BaseExtractor

    transformer: BaseTransformer

    validator: BaseValidator

    loader: BaseLoader