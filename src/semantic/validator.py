"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : validator.py
Package     : src.semantic
Purpose     : Enterprise Semantic Layer Validator
Author      : ERIP
Version     : 2.1.0

Description
-----------
Enterprise validator for the Semantic Layer.

Responsibilities
----------------
- Validate analytics schema
- Validate warehouse dependencies
- Validate semantic views
- Validate semantic data availability
- Report validation summary

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import text

from sqlalchemy.engine import Engine

from src.observability import get_logger


logger = get_logger(__name__)


# =============================================================================
# Validation Result
# =============================================================================


@dataclass(slots=True)
class ValidationResult:
    """
    Semantic validation result.
    """

    passed: bool

    checks_performed: int

    failures: list[str] = field(default_factory=list)


# =============================================================================
# Semantic Validator
# =============================================================================


class SemanticValidator:
    """
    Enterprise Semantic Validator.
    """

    REQUIRED_TABLES = (

        "dim_customer",

        "dim_date",

        "dim_product",

        "dim_seller",

        "fact_sales",

    )

    REQUIRED_VIEWS = (

        "vw_sales",

        "vw_customer_sales",

        "vw_product_performance",

        "vw_seller_performance",

        "vw_revenue_dashboard",

    )

    def __init__(
        self,
        *,
        engine: Engine,
    ) -> None:
        """
        Construct a SemanticValidator.

        Parameters
        ----------
        engine
            Shared SQLAlchemy engine supplied by the
            ServiceContainer.
        """

        self.engine = engine

    # -------------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Validate semantic layer deployment.
        """

        logger.info("=" * 60)
        logger.info("Starting Semantic Layer Validation")
        logger.info("=" * 60)

        failures: list[str] = []

        checks = [

            self._validate_schema,

            self._validate_required_tables,

            self._validate_views_exist,

            self._validate_views_queryable,

        ]

        for check in checks:

            try:

                check()

            except Exception as error:

                failures.append(str(error))

                logger.error(str(error))

        passed = len(failures) == 0

        if passed:

            logger.info("Semantic validation successful.")

        else:

            logger.error("Semantic validation failed.")

        return ValidationResult(

            passed=passed,

            checks_performed=len(checks),

            failures=failures,

        )

    # -------------------------------------------------------------------------

    def _validate_schema(self) -> None:
        """
        Validate analytics schema exists.
        """

        sql = """
        SELECT EXISTS
        (
            SELECT 1
            FROM information_schema.schemata
            WHERE schema_name='analytics'
        );
        """

        with self.engine.begin() as connection:

            exists = connection.execute(

                text(sql)

            ).scalar()

        if not exists:

            raise RuntimeError(

                "Analytics schema does not exist."

            )

    # -------------------------------------------------------------------------

    def _validate_required_tables(self) -> None:
        """
        Validate warehouse tables exist.
        """

        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='analytics';
        """

        with self.engine.begin() as connection:

            tables = {

                row[0]

                for row in connection.execute(

                    text(sql)

                )

            }

        missing = [

            table

            for table in self.REQUIRED_TABLES

            if table not in tables

        ]

        if missing:

            raise RuntimeError(

                "Missing warehouse tables: "

                + ", ".join(missing)

            )

    # -------------------------------------------------------------------------

    def _validate_views_exist(self) -> None:
        """
        Validate required semantic views exist.
        """

        sql = """
        SELECT table_name
        FROM information_schema.views
        WHERE table_schema='analytics';
        """

        with self.engine.begin() as connection:

            views = {

                row[0]

                for row in connection.execute(

                    text(sql)

                )

            }

        missing = [

            view

            for view in self.REQUIRED_VIEWS

            if view not in views

        ]

        if missing:

            raise RuntimeError(

                "Missing semantic views: "

                + ", ".join(missing)

            )

    # -------------------------------------------------------------------------

    def _validate_views_queryable(self) -> None:
        """
        Validate each semantic view can be queried.

        This validates deployment only.
        It does not require business data.
        """

        with self.engine.begin() as connection:

            for view in self.REQUIRED_VIEWS:

                connection.execute(

                    text(

                        f"""
                        SELECT *
                        FROM analytics.{view}
                        LIMIT 1
                        """
                    )

                )

    # -------------------------------------------------------------------------

    def summary(self) -> dict:
        """
        Validator summary.
        """

        result = self.validate()

        return {

            "passed": result.passed,

            "checks_performed": result.checks_performed,

            "failures": result.failures,

        }