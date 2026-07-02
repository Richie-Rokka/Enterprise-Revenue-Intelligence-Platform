"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : metadata_builder.py
Package     : src.etl.metadata
Purpose     : Enterprise Metadata Builder
Author      : ERIP
Version     : 3.0.0

Description
-----------
Builds enterprise metadata columns for datasets prior to loading.

Responsibilities
----------------
• Generate Batch ID
• Generate Load ID
• Generate Row Hash
• Add Source Metadata
• Add ETL Version
• Preserve Business Columns

Notes
-----
Stateless utility.

No database dependency.

===============================================================================
"""

from __future__ import annotations

import hashlib
import uuid

import pandas as pd


class MetadataBuilder:
    """
    Enterprise metadata builder.
    """

    EXCLUDED_COLUMNS = {

        "source_system_code",

        "source_file",

        "batch_id",

        "load_id",

        "etl_version",

        "row_hash",

        "validation_status_code",

        "record_status_code",

        "source_created_at",

        "source_updated_at",

        "ingested_at",

    }

    # ---------------------------------------------------------------------

    def __init__(

        self,

        source_system: str,

        source_file: str,

        etl_version: str,

    ) -> None:

        self.source_system = source_system

        self.source_file = source_file

        self.etl_version = etl_version

        self.batch_id = str(uuid.uuid4())

        self.load_id = str(uuid.uuid4())

    # ---------------------------------------------------------------------

    def build(

        self,

        dataframe: pd.DataFrame,

    ) -> pd.DataFrame:
        """
        Add enterprise metadata columns.
        """

        dataframe = dataframe.copy()

        dataframe["source_system_code"] = self.source_system

        dataframe["source_file"] = self.source_file

        dataframe["batch_id"] = self.batch_id

        dataframe["load_id"] = self.load_id

        dataframe["etl_version"] = self.etl_version

        dataframe["row_hash"] = self._row_hash(dataframe)

        return dataframe

    # ---------------------------------------------------------------------

    def _row_hash(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.Series:
        """
        Generate deterministic SHA256 hash
        for each business record.
        """

        business_columns = sorted(

            column

            for column in dataframe.columns

            if column not in self.EXCLUDED_COLUMNS

        )

        business_df = (

            dataframe[business_columns]

            .copy()

            .fillna("")

        )

        return business_df.apply(

            lambda row: hashlib.sha256(

                "|".join(

                    str(value)

                    for value in row

                ).encode("utf-8")

            ).hexdigest(),

            axis=1,

        )