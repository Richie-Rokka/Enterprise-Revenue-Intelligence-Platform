"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : validator.py
Package     : src.semantic
Purpose     : Semantic Layer Validator
Author      : ERIP
Version     : 2.0.0

Description
-----------
Validates the deployed Semantic Layer after SQL execution.

Responsibilities
----------------
- Validate semantic deployment
- Report validation failures
- Provide deployment readiness

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import text

from src.database.connection import get_engine
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

    failures: list[str] = field(default_factory=list)


# =============================================================================
# Validator
# =============================================================================


class SemanticValidator:
    """
    Enterprise Semantic Validator.
    """

    def __init__(self) -> None:

        self.engine = get_engine()

    # -------------------------------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Validate semantic layer deployment.
        """

        failures: list[str] = []

        checks = [

            self._validate_schema,

            self._validate_views,

        ]

        for check in checks:

            try:

                check()

            except Exception as error:

                failures.append(str(error))

        if failures:

            logger.error(
                "Semantic validation failed."
            )

        else:

            logger.info(
                "Semantic validation passed."
            )

        return ValidationResult(

            passed=len(failures) == 0,

            failures=failures,
        )

    # -------------------------------------------------------------------------

    def _validate_schema(self) -> None:
        """
        Validate analytics schema exists.
        """

        sql = """
        SELECT EXISTS (

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

                "Schema 'analytics' does not exist."

            )

    # -------------------------------------------------------------------------

    def _validate_views(self) -> None:
        """
        Validate at least one analytics view exists.
        """

        sql = """
        SELECT COUNT(*)

        FROM information_schema.views

        WHERE table_schema='analytics';
        """

        with self.engine.begin() as connection:

            count = connection.execute(

                text(sql)

            ).scalar()

        if count == 0:

            raise RuntimeError(

                "No analytics views found."

            )