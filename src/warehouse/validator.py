"""
Enterprise Revenue Intelligence Platform (ERIP)

Warehouse Validator

Validates the warehouse after deployment to ensure
required schemas and tables exist before ETL execution.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text

from src.database import get_engine
from src.observability import get_logger
from src.config.config import config


logger = get_logger(__name__)


@dataclass(slots=True)
class ValidationResult:
    """
    Warehouse validation result.
    """

    passed: bool

    checks_performed: int

    failures: list[str]


class WarehouseValidator:
    """
    Enterprise Warehouse Validator.
    """

    def __init__(self):

        self.engine = get_engine()

    def _schema_exists(
        self,
        schema: str,
    ) -> bool:
        """
        Check whether a schema exists.
        """

        query = text(
            """
            SELECT EXISTS (

                SELECT 1

                FROM information_schema.schemata

                WHERE schema_name = :schema

            )
            """
        )

        with self.engine.connect() as connection:

            return bool(

                connection.execute(

                    query,

                    {"schema": schema},

                ).scalar()

            )

    def _table_exists(
        self,
        schema: str,
        table: str,
    ) -> bool:
        """
        Check whether a table exists.
        """

        query = text(
            """
            SELECT EXISTS (

                SELECT 1

                FROM information_schema.tables

                WHERE table_schema = :schema

                AND table_name = :table

            )
            """
        )

        with self.engine.connect() as connection:

            return bool(

                connection.execute(

                    query,

                    {

                        "schema": schema,

                        "table": table,

                    },

                ).scalar()

            )

    def validate(self) -> ValidationResult:
        """
        Validate warehouse deployment.
        """

        logger.info(
            "Starting warehouse validation..."
        )

        failures = []

        checks = 0

        required_schemas = [

            config.database.schemas.staging,

            config.database.schemas.analytics,

            config.database.schemas.monitoring,

        ]

        for schema in required_schemas:

            checks += 1

            if not self._schema_exists(schema):

                failures.append(

                    f"Missing schema: {schema}"

                )

        required_tables = [

            ("analytics", "dim_customer"),

            ("analytics", "dim_product"),

            ("analytics", "dim_seller"),

            ("analytics", "dim_date"),

            ("analytics", "fact_sales"),

        ]

        for schema, table in required_tables:

            checks += 1

            if not self._table_exists(
                schema,
                table,
            ):

                failures.append(

                    f"Missing table: {schema}.{table}"

                )

        if failures:

            logger.error(
                "Warehouse validation failed."
            )

        else:

            logger.info(
                "Warehouse validation successful."
            )

        return ValidationResult(

            passed=len(failures) == 0,

            checks_performed=checks,

            failures=failures,

        )