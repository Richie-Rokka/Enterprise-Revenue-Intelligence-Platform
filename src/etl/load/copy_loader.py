"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : copy_loader.py
Package     : src.etl.load
Purpose     : PostgreSQL COPY Engine
Author      : ERIP
Version     : 3.0.0

Description
-----------
Provides high-performance PostgreSQL COPY loading for pandas DataFrames.

Responsibilities
----------------
• Determine matching table columns
• Serialize DataFrame to CSV buffer
• Execute PostgreSQL COPY
• Return rows loaded

Notes
-----
Contains no business logic.

Does not manage transactions.

Does not open or close database connections.

===============================================================================
"""

from __future__ import annotations

import csv
import io

import pandas as pd

from psycopg2.extensions import connection


class CopyLoader:
    """
    Enterprise PostgreSQL COPY loader.
    """

    # ---------------------------------------------------------------------

    def __init__(
        self,
        connection: connection,
    ) -> None:

        self.connection = connection

    # ---------------------------------------------------------------------

    def table_columns(
        self,
        target_table: str,
    ) -> list[str]:
        """
        Retrieve target table columns.
        """

        schema, table = target_table.split(".")

        sql = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s
              AND table_name = %s
            ORDER BY ordinal_position;
        """

        with self.connection.cursor() as cursor:

            cursor.execute(

                sql,

                (

                    schema,

                    table,

                ),

            )

            return [

                row[0]

                for row in cursor.fetchall()

            ]

    # ---------------------------------------------------------------------

    def load(
        self,
        dataframe: pd.DataFrame,
        target_table: str,
    ) -> int:
        """
        Load a DataFrame using PostgreSQL COPY.

        Returns
        -------
        int
            Number of rows loaded.
        """

        database_columns = self.table_columns(

            target_table

        )

        load_columns = [

            column

            for column in database_columns

            if column in dataframe.columns

        ]

        if not load_columns:

            raise ValueError(

                f"No matching columns found for {target_table}."

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

            f"COPY {target_table} "

            f"({', '.join(load_columns)}) "

            f"FROM STDIN "

            f"WITH (FORMAT CSV)"

        )

        with self.connection.cursor() as cursor:

            cursor.copy_expert(

                sql=sql,

                file=buffer,

            )

        return len(dataframe)