"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_staging_tables.py

Purpose:
    Validate all ERIP staging tables.

Description:
    Verifies that every required staging table exists in the warehouse.

Validated Tables
----------------
• customer
• product
• seller
• geolocation
• product_category_translation
• sales_order
• sales_order_item
• sales_order_payment
• sales_order_review

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


class StagingValidator(BaseValidator):
    """
    Validates all required staging tables.
    """

    NAME = "Staging Tables"

    REQUIRED_TABLES = (
        "customer",
        "product",
        "seller",
        "geolocation",
        "product_category_translation",
        "sales_order",
        "sales_order_item",
        "sales_order_payment",
        "sales_order_review",
    )

    # -------------------------------------------------------------------------

    def validate(self):

        try:

            existing = []
            missing = []

            for table in self.REQUIRED_TABLES:

                if self.table_exists("staging", table):

                    existing.append(table)

                else:

                    missing.append(table)

            if missing:

                return self.failure(
                    self.NAME,
                    "Missing staging tables: "
                    + ", ".join(missing)
                )

            return self.success(
                self.NAME,
                (
                    f"Validated "
                    f"{len(existing)} staging tables."
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

    validator = StagingValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("STAGING TABLE VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)