"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_metadata.py

Purpose:
    Validate the ERIP metadata framework.

Description:
    Verifies that all required metadata reference tables have been
    successfully deployed.

Validated Tables
----------------
• metadata.ref_validation_status
• metadata.ref_record_status
• metadata.ref_source_system
• metadata.ref_etl_version

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


class MetadataValidator(BaseValidator):
    """
    Validates ERIP metadata reference tables.
    """

    NAME = "Metadata Framework"

    REQUIRED_TABLES = (
        "ref_validation_status",
        "ref_record_status",
        "ref_source_system",
        "ref_etl_version",
    )

    # -------------------------------------------------------------------------

    def validate(self):

        try:

            missing = [
                table
                for table in self.REQUIRED_TABLES
                if not self.table_exists("metadata", table)
            ]

            if missing:

                return self.failure(
                    self.NAME,
                    "Missing metadata tables: " + ", ".join(missing)
                )

            return self.success(
                self.NAME,
                f"Validated {len(self.REQUIRED_TABLES)} metadata tables."
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

    validator = MetadataValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("METADATA VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)