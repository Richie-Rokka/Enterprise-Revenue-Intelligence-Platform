"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module      : load_staging.py
Package     : src.load
Purpose     : Enterprise Staging Data Orchestrator
Version     : 2.0.0
===============================================================================
"""

from __future__ import annotations

import time

import psycopg2

from src.config.config import config
from src.observability.logger import get_logger

from src.load.load_customer import CustomerLoader
from src.load.load_product import ProductLoader
from src.load.load_seller import SellerLoader
from src.load.load_geolocation import GeolocationLoader
from src.load.load_product_category_translation import (
    ProductCategoryTranslationLoader,
)
from src.load.load_orders import OrdersLoader
from src.load.load_order_items import OrderItemsLoader
from src.load.load_order_payments import OrderPaymentsLoader
from src.load.load_order_reviews import OrderReviewsLoader


LOGGER = get_logger(__name__)


LOADERS = [
    ProductCategoryTranslationLoader,
    CustomerLoader,
    ProductLoader,
    SellerLoader,
    GeolocationLoader,
    OrdersLoader,
    OrderItemsLoader,
    OrderPaymentsLoader,
    OrderReviewsLoader,
]


def analyze_tables(connection) -> None:

    LOGGER.info("Refreshing PostgreSQL statistics...")

    tables = [
        "staging.product_category_translation",
        "staging.customer",
        "staging.product",
        "staging.seller",
        "staging.geolocation",
        "staging.orders",
        "staging.order_items",
        "staging.order_payments",
        "staging.order_reviews",
    ]

    with connection.cursor() as cursor:

        for table in tables:

            cursor.execute(
                f"ANALYZE {table};"
            )


def main() -> None:

    start_time = time.perf_counter()

    db = config.database

    LOGGER.info("=" * 70)
    LOGGER.info("ERIP STAGING DATA LOAD")
    LOGGER.info("=" * 70)

    connection = None

    loaders_completed = 0

    try:

        connection = psycopg2.connect(
            host=db.host,
            port=db.port,
            database=db.database,
            user=db.username,
            password=db.password,
        )

        connection.autocommit = False

        for loader_class in LOADERS:

            loader = loader_class()

            loader.connection = connection
            loader.owns_connection = False

            LOGGER.info(
                "Loading %s...",
                loader.target_table,
            )

            loader.run()

            loaders_completed += 1

        analyze_tables(connection)

        connection.commit()

        duration = round(
            time.perf_counter() - start_time,
            3,
        )

        LOGGER.info("=" * 70)
        LOGGER.info("ERIP STAGING LOAD COMPLETED")
        LOGGER.info("=" * 70)
        LOGGER.info(
            "Datasets Loaded : %d",
            loaders_completed,
        )
        LOGGER.info(
            "Execution Time  : %.3f sec",
            duration,
        )
        LOGGER.info(
            "Status          : SUCCESS"
        )
        LOGGER.info("=" * 70)

    except Exception:

        if connection is not None:

            connection.rollback()

        LOGGER.exception(
            "Staging load failed."
        )

        raise

    finally:

        if connection is not None:

            connection.close()

            LOGGER.info(
                "Database connection closed."
            )


if __name__ == "__main__":
    main()