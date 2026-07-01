"""
loader.py
Enterprise Revenue Intelligence Platform

Purpose
-------
Centralized loading framework.

Version 1.1
-----------
Dimension tables : DELETE + INSERT
Fact tables      : TRUNCATE + INSERT
"""

from time import perf_counter
from sqlalchemy import text

from src.utils.logger import (
    get_logger,
    log_success
)

logger = get_logger(__name__)

TABLE_CONFIG = {
    "dim_customer": {"type": "dimension"},
    "dim_product": {"type": "dimension"},
    "dim_seller": {"type": "dimension"},
    "dim_date": {"type": "dimension"},
    "fact_sales": {"type": "fact"},
}


def load_table(
    engine,
    dataframe,
    table_name,
    schema="analytics"
):
    if table_name not in TABLE_CONFIG:
        raise ValueError(
            f"No loader configuration for {table_name}"
        )

    table_type = TABLE_CONFIG[table_name]["type"]
    full_table = f"{schema}.{table_name}"

    logger.info(
        f"Loading {full_table} ({table_type})"
    )

    start = perf_counter()

    try:

        with engine.begin() as connection:

            if table_type == "dimension":

                connection.execute(
                    text(
                        f"DELETE FROM {full_table};"
                    )
                )

            elif table_type == "fact":

                connection.execute(
                    text(
                        f"TRUNCATE TABLE {full_table} RESTART IDENTITY;"
                    )
                )

        dataframe.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists="append",
            index=False,
            method="multi"
        )

        load_time = round(
            perf_counter() - start,
            2
        )

        rows_loaded = len(dataframe)

        log_success(
            logger,
            f"{rows_loaded:,} rows loaded into {full_table}"
        )

        log_success(
            logger,
            f"Database Load Time: {load_time:.2f} seconds"
        )

        return {
            "table": table_name,
            "rows_loaded": rows_loaded,
            "load_time_seconds": load_time
        }

    except Exception as error:

        logger.exception(
            f"Failed loading {full_table}: {error}"
        )

        raise
