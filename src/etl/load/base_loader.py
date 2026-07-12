"""
===============================================================================
Enterprise Load framework.

Responsibilities
----------------
• Persist validated datasets
• Enrich enterprise metadata
• Execute PostgreSQL COPY
• Manage transactions
• Produce LoadResult

This class represents the canonical "L" stage of the
Enterprise ETL Pipeline.

Module      : base_loader.py
Package     : src.load
Purpose     : Enterprise Base Loader Framework
Version     : 3.3.0
===============================================================================
"""

from __future__ import annotations

import csv
import hashlib
import io
import time
import uuid

from abc import ABC
from pathlib import Path
from typing import Iterable

import pandas as pd
import psycopg2

from psycopg2.extensions import connection

from src.config.config import config
from src.observability.logger import get_logger
from src.observability.memory import get_memory_usage
from src.etl.metadata.metadata_builder import MetadataBuilder
from src.etl.results import LoadResult
from src.etl.context import ETLContext


class BaseLoader(ABC):
    """
    Enterprise staging loader framework.
    """

    def __init__(
        self,
        source_file: str | Path,
        target_table: str,
        required_columns: Iterable[str],
        context: ETLContext | None = None,
        connection: connection | None = None,
        truncate_before_load: bool = True,
        remove_duplicates: bool = False,
    ) -> None:

        self.root_dir = Path(__file__).resolve().parents[3]

        self.source_file = self.root_dir / Path(source_file)

        self.target_table = target_table

        self.required_columns = list(required_columns)

        self.connection = connection

        self.owns_connection = connection is None

        self.truncate_before_load = truncate_before_load

        self.remove_duplicates = remove_duplicates

        self.logger = get_logger(self.__class__.__name__)

        self.context = context

        # ---------------------------------------------------------------------
        # Enterprise Metadata
        # ---------------------------------------------------------------------

        self.source_system_code = "OLIST"

        self.batch_id = uuid.uuid4()

        self.load_id = uuid.uuid4()

        self.etl_version = "3.2.0"

        # ---------------------------------------------------------------------
        # Runtime Metrics
        # ---------------------------------------------------------------------

        self.rows_read = 0
        self.rows_loaded = 0
        self.rows_rejected = 0

        self.start_time = 0.0
        self.end_time = 0.0

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------

    def connect(self) -> None:

        if self.connection is not None:
            return

        db = config.database

        self.connection = psycopg2.connect(
            host=db.host,
            port=db.port,
            database=db.database,
            user=db.username,
            password=db.password,
        )

        self.connection.autocommit = False

        self.logger.info(
            "Connected to PostgreSQL database '%s'.",
            db.database,
        )

    def disconnect(self) -> None:

        if not self.owns_connection:
            return

        if self.connection is not None:

            self.connection.close()

            self.connection = None

            self.logger.info(
                "Database connection closed."
            )

    # Legacy extension hook.
    #
    # Retained for backward compatibility during the migration.

    # -------------------------------------------------------------------------
    # Hooks
    # -------------------------------------------------------------------------

    def before_load(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        return dataframe

    def after_load(self) -> None:

        pass

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def table_columns(self) -> list[str]:

        if self.connection is None:

            raise RuntimeError(
                "Database connection not established."
            )

        schema, table = self.target_table.split(".")

        query = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema=%s
              AND table_name=%s
            ORDER BY ordinal_position;
        """

        with self.connection.cursor() as cursor:

            cursor.execute(
                query,
                (schema, table),
            )

            return [
                row[0]
                for row in cursor.fetchall()
            ]

    # -------------------------------------------------------------------------
    # Legacy Compatibility Layer (Deprecated)
    #
    # These methods support the legacy standalone loader execution model.
    #
    # They will be removed after every dataset has been migrated to the
    # enterprise ETLPipeline architecture.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # CSV
    # -------------------------------------------------------------------------

    def read_csv(self) -> pd.DataFrame:

        if not self.source_file.exists():

            raise FileNotFoundError(
                f"Source file not found: {self.source_file}"
            )

        self.logger.info(
            "Reading %s...",
            self.source_file.name,
        )

        dataframe = pd.read_csv(
            self.source_file,
            low_memory=False,
            keep_default_na=False,
        )

        self.rows_read = len(dataframe)

        self.logger.info(
            f"Rows read: {self.rows_read:,}"
        )

        return dataframe
    
    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def validate(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        dataframe.columns = (
            dataframe.columns
            .str.strip()
            .str.lower()
        )

        missing = [
            column
            for column in self.required_columns
            if column not in dataframe.columns
        ]

        if missing:

            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )

    # -------------------------------------------------------------------------
    # Cleaning
    # -------------------------------------------------------------------------

    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe.columns = (
            dataframe.columns
            .str.strip()
            .str.lower()
        )

        dataframe = dataframe.replace("", None)

        if self.remove_duplicates:

            before = len(dataframe)

            dataframe = dataframe.drop_duplicates()

            removed = before - len(dataframe)

            if removed > 0:

                self.logger.info(
                    f"Removed {removed:,} duplicate rows."
                )

        return dataframe

    # -------------------------------------------------------------------------
    # Enterprise Metadata
    # -------------------------------------------------------------------------

    def calculate_row_hash(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.Series:

        excluded_columns = {
            "source_system_code",
            "source_file",
            "batch_id",
            "load_id",
            "source_created_at",
            "source_updated_at",
            "ingested_at",
            "row_hash",
            "etl_version",
            "validation_status_code",
            "record_status_code",
        }

        business_columns = [
            column
            for column in dataframe.columns
            if column not in excluded_columns
        ]

        return (
            dataframe[business_columns]
            .fillna("")
            .astype(str)
            .agg("|".join, axis=1)
            .apply(
                lambda value: hashlib.sha256(
                    value.encode("utf-8")
                ).hexdigest()
            )
        )

    def add_metadata(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe = dataframe.copy()

        dataframe["source_system_code"] = self.source_system_code

        dataframe["source_file"] = self.source_file.name

        dataframe["batch_id"] = str(self.batch_id)

        dataframe["load_id"] = str(self.load_id)

        dataframe["etl_version"] = self.etl_version

        dataframe["row_hash"] = self.calculate_row_hash(
            dataframe
        )

        return dataframe

    # -------------------------------------------------------------------------
    # Staging
    # -------------------------------------------------------------------------

    def truncate_table(self) -> None:

        if not self.truncate_before_load:
            return

        if self.connection is None:

            raise RuntimeError(
                "Database connection not established."
            )

        self.logger.info(
            "Truncating %s...",
            self.target_table,
        )

        with self.connection.cursor() as cursor:

            cursor.execute(
                f"TRUNCATE TABLE {self.target_table};"
            )

    # -------------------------------------------------------------------------
    # COPY
    # -------------------------------------------------------------------------

    def copy_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        if self.connection is None:

            raise RuntimeError(
                "Database connection not established."
            )

        database_columns = self.table_columns()

        load_columns = [
            column
            for column in database_columns
            if column in dataframe.columns
        ]

        if not load_columns:

            raise ValueError(
                f"No matching columns found for {self.target_table}."
            )

        dataframe = dataframe.loc[:, load_columns]

        buffer = io.StringIO()

        dataframe.to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="",
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n",
        )

        buffer.seek(0)

        sql = (
            f"COPY {self.target_table} "
            f"({', '.join(load_columns)}) "
            f"FROM STDIN "
            f"WITH (FORMAT CSV)"
        )

        self.logger.info(
            f"Loading {len(load_columns)} columns into {self.target_table}."
        )

        with self.connection.cursor() as cursor:

            cursor.copy_expert(
                sql=sql,
                file=buffer,
            )

        self.rows_loaded = len(dataframe)

        self.logger.info(
            f"Rows loaded: {self.rows_loaded:,}"
        )

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    def summary(self) -> None:

        memory = get_memory_usage()

        duration = round(
            self.end_time - self.start_time,
            3,
        )

        self.logger.info("=" * 70)
        self.logger.info("ERIP STAGING LOAD SUMMARY")
        self.logger.info("=" * 70)

        self.logger.info(
            "Source File   : %s",
            self.source_file.name,
        )

        self.logger.info(
            "Target Table  : %s",
            self.target_table,
        )

        self.logger.info(
            "Rows Read     : %s",
            f"{self.rows_read:,}",
        )

        self.logger.info(
            "Rows Loaded   : %s",
            f"{self.rows_loaded:,}",
        )

        self.logger.info(
            "Rows Rejected : %s",
            f"{self.rows_rejected:,}",
        )

        self.logger.info(
            "Memory Usage  : %.2f MB",
            memory.current_mb,
        )

        self.logger.info(
        "Execution     : %.3f sec",
            duration,
        )

        status = (
            self.context.status
            if self.context is not None
            else "SUCCESS"
        )

        self.logger.info(
            "Status        : %s",
            status,
        )

        self.logger.info("=" * 70)

    # -------------------------------------------------------------------------
    # Enterprise Load API
    # -------------------------------------------------------------------------

    def load(
        self,
        dataframe: pd.DataFrame,
    ) -> LoadResult:
        """
        Enterprise loading API.

        This method represents the canonical "Load" stage of the
        enterprise ETL pipeline.

        Expected input:
            - Extracted
            - Transformed
            - Validated

        The loader is responsible only for persistence,
        metadata enrichment and transaction management.

        Returns
        -------
        int
            Number of rows successfully loaded.
        """

        try:

            self.start_time = time.perf_counter()

            self.connect()

            builder = MetadataBuilder(

                source_system=self.source_system_code,

                source_file=self.source_file.name,

                etl_version=self.etl_version,

            )

            dataframe = builder.build(dataframe)

            self.truncate_table()

            self.copy_dataframe(dataframe)

            self.after_load()

            self.after_load()

            if self.context is not None:

                self.context.add_rows_loaded(
                    self.rows_loaded
                )

            if self.connection is not None and self.owns_connection:

                self.connection.commit()

            self.end_time = time.perf_counter()

            if self.context is not None:

                self.rows_read = self.context.rows_extracted

                self.context.finish()

            # -----------------------------------------------------------------
            # Synchronize enterprise ETL context metrics with legacy loader
            # summary during migration.
            # -----------------------------------------------------------------

            if self.context is not None:

                self.rows_read = self.context.rows_extracted

            self.summary()

            duration = round(
                self.end_time - self.start_time,
                3,
            )

            return LoadResult(

                target_table=self.target_table,

                rows_loaded=self.rows_loaded,

                rows_rejected=self.rows_rejected,

                batch_id=self.batch_id,

                load_id=self.load_id,

                duration_seconds=duration,

                success=True,

            )

        except Exception:

            self.rows_rejected = len(dataframe)

            if (
                self.connection is not None
                and self.owns_connection
            ):

                self.connection.rollback()

            self.logger.exception(
                "Failed loading %s",
                self.target_table,
            )

            raise

        finally:

            self.disconnect()

        """
        DEPRECATED

        Use:

            ETLPipeline.execute()

        instead.

        This method exists only to support datasets that have not yet
        been migrated to the enterprise pipeline.
        """

    # -------------------------------------------------------------------------
    # Pipeline
    # -------------------------------------------------------------------------

    def run(self) -> None:

        try:

            self.start_time = time.perf_counter()

            self.connect()

            dataframe = self.read_csv()

            self.validate(dataframe)

            dataframe = self.clean(dataframe)

            dataframe = self.before_load(dataframe)

            result = self.load(dataframe)

            return result

        except Exception as ex:

            self.rows_rejected = self.rows_read

            if (
                self.connection is not None
                and self.owns_connection
            ):

                self.connection.rollback()

            self.logger.exception(
                "Failed loading %s: %s",
                self.target_table,
                ex,
            )

            raise

        finally:

            self.disconnect()