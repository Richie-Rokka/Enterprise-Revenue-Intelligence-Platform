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
from src.etl.results import PipelineResult


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

    def execute(self) -> PipelineResult:
        """
        Execute the complete ETL pipeline.
        """

        try:

            # --------------------------------------------------------------
            # Extract
            # --------------------------------------------------------------

            raw_dataframe = self.extractor.extract()

            rows_extracted = len(raw_dataframe)

            # --------------------------------------------------------------
            # Transform
            # --------------------------------------------------------------

            transformed_dataframe = self.transformer.transform(
                raw_dataframe
            )

            rows_transformed = len(transformed_dataframe)

            # --------------------------------------------------------------
            # Validate
            # --------------------------------------------------------------

            validated_dataframe = self.validator.validate(
                transformed_dataframe
            )

            rows_validated = len(validated_dataframe)

            # --------------------------------------------------------------
            # Load
            # --------------------------------------------------------------

            load_result = self.loader.load(
                validated_dataframe
            )

            
            return PipelineResult(

                pipeline_name=self.name,

                rows_extracted=rows_extracted,

                rows_transformed=rows_transformed,

                rows_validated=rows_validated,

                load_result=load_result,

            )

        except Exception as ex:

            self.context.mark_failed(
                str(ex)
            )

            raise