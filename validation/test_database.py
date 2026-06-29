"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_database.py

Purpose:
    Validate PostgreSQL connectivity and health.

Description:
    Performs the foundational validation for the ERIP platform by verifying:

    • Database connectivity
    • Authentication
    • Active database
    • PostgreSQL server health

Author:
    Abodunrin Oketade

Platform:
    Enterprise Revenue Intelligence Platform (ERIP)

Version:
    2.0.0
===============================================================================
"""

from __future__ import annotations

from src.database.health import check_database_health

from validation.base import BaseValidator


class DatabaseValidator(BaseValidator):
    """
    Validates PostgreSQL connectivity and health.
    """

    NAME = "Database Connection"

    def __init__(self) -> None:

        super().__init__()

        

    # -------------------------------------------------------------------------

    def validate(self):

        try:

            health = check_database_health()

            if health["status"] != "Healthy":

                return self.failure(
                    self.NAME,
                    "Database health check failed."
                )

            return self.success(
                self.NAME,
                (
                    f"Connected to "
                    f"{health['database']} "
                    f"({health['version']})"
                )
            )

        except Exception as exc:

            return self.failure(
                self.NAME,
                str(exc)
            )


# ==============================================================================
# STANDALONE EXECUTION
# ==============================================================================

if __name__ == "__main__":

    validator = DatabaseValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("DATABASE VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)