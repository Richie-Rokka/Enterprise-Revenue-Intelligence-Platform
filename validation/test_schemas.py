"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_schemas.py

Purpose:
    Validate the existence of all required ERIP database schemas.

Description:
    Verifies that the warehouse foundation has been correctly deployed by
    ensuring all required schemas exist in the target PostgreSQL database.

Validated Schemas
-----------------
• staging
• analytics
• metadata
• monitoring

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


class SchemaValidator(BaseValidator):
    """
    Validates the existence of all required ERIP schemas.
    """

    NAME = "Warehouse Schemas"

    REQUIRED_SCHEMAS = (
        "staging",
        "analytics",
        "metadata",
        "monitoring",
    )

    # -------------------------------------------------------------------------

    def validate(self):

        try:

            missing = [
                schema
                for schema in self.REQUIRED_SCHEMAS
                if not self.schema_exists(schema)
            ]

            if missing:

                return self.failure(
                    self.NAME,
                    "Missing schemas: " + ", ".join(missing)
                )

            return self.success(
                self.NAME,
                f"Validated {len(self.REQUIRED_SCHEMAS)} schemas."
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

    validator = SchemaValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("SCHEMA VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)