"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_warehouse.py

Purpose:
    Validate the overall ERIP warehouse.

Description:
    Performs high-level warehouse validation to ensure that the
    warehouse foundation is complete and operational.

Validation Scope
----------------
• Required schemas exist
• Required metadata tables exist
• Required staging tables exist
• Warehouse object counts

Author:
    Abodunrin Oketade

Platform:
    Enterprise Revenue Intelligence Platform (ERIP)

Version:
    2.0.0
===============================================================================
"""

from __future__ import annotations

from validation.base import BaseValidator


class WarehouseValidator(BaseValidator):
    """
    Performs high-level warehouse validation.
    """

    NAME = "Warehouse"

    EXPECTED_SCHEMAS = 4

    EXPECTED_METADATA_TABLES = 4

    EXPECTED_STAGING_TABLES = 9

    # -------------------------------------------------------------------------

    def validate(self):

        try:

            schema_count = self.execute_scalar(
                """
                SELECT COUNT(*)
                FROM information_schema.schemata
                WHERE schema_name IN
                (
                    'staging',
                    'analytics',
                    'metadata',
                    'monitoring'
                );
                """
            )

            metadata_count = self.execute_scalar(
                """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'metadata';
                """
            )

            staging_count = self.execute_scalar(
                """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'staging';
                """
            )

            failures = []

            if schema_count != self.EXPECTED_SCHEMAS:

                failures.append(
                    f"Schemas ({schema_count}/{self.EXPECTED_SCHEMAS})"
                )

            if metadata_count < self.EXPECTED_METADATA_TABLES:

                failures.append(
                    f"Metadata Tables ({metadata_count}/{self.EXPECTED_METADATA_TABLES})"
                )

            if staging_count < self.EXPECTED_STAGING_TABLES:

                failures.append(
                    f"Staging Tables ({staging_count}/{self.EXPECTED_STAGING_TABLES})"
                )

            if failures:

                return self.failure(
                    self.NAME,
                    "; ".join(failures)
                )

            return self.success(
                self.NAME,
                (
                    "Warehouse structure validated "
                    f"({schema_count} schemas, "
                    f"{metadata_count} metadata tables, "
                    f"{staging_count} staging tables)."
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

    validator = WarehouseValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("WAREHOUSE VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)