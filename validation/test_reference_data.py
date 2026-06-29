"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_reference_data.py

Purpose:
    Validate ERIP reference data.

Description:
    Verifies that all required reference data has been successfully seeded
    into the metadata schema.

Validated Reference Data
------------------------
Validation Status
    • PENDING
    • VALID
    • INVALID
    • REJECTED

Record Status
    • ACTIVE
    • UPDATED
    • DELETED
    • ARCHIVED

Source System
    • OLIST

ETL Version
    • 2.0.0

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


class ReferenceDataValidator(BaseValidator):
    """
    Validates enterprise reference data.
    """

    NAME = "Reference Data"

    # -------------------------------------------------------------------------

    def validate(self):

        try:

            checks = [

                (
                    """
                    SELECT COUNT(*)
                    FROM metadata.ref_validation_status
                    WHERE validation_status_code IN
                    ('PENDING','VALID','INVALID','REJECTED')
                    """,
                    4,
                    "Validation Status"
                ),

                (
                    """
                    SELECT COUNT(*)
                    FROM metadata.ref_record_status
                    WHERE record_status_code IN
                    ('ACTIVE','UPDATED','DELETED','ARCHIVED')
                    """,
                    4,
                    "Record Status"
                ),

                (
                    """
                    SELECT COUNT(*)
                    FROM metadata.ref_source_system
                    WHERE source_system_code = 'OLIST'
                    """,
                    1,
                    "Source System"
                ),

                (
                    """
                    SELECT COUNT(*)
                    FROM metadata.ref_etl_version
                    WHERE etl_version = '2.0.0'
                    """,
                    1,
                    "ETL Version"
                )

            ]

            failures = []

            for query, expected, description in checks:

                actual = self.execute_scalar(query)

                if actual != expected:

                    failures.append(
                        f"{description} ({actual}/{expected})"
                    )

            if failures:

                return self.failure(
                    self.NAME,
                    "Missing or invalid reference data: "
                    + "; ".join(failures)
                )

            return self.success(
                self.NAME,
                "All enterprise reference data validated."
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

    validator = ReferenceDataValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("REFERENCE DATA VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)