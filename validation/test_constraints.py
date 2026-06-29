"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_constraints.py

Purpose:
    Validate database constraints for the ERIP warehouse.

Description:
    Verifies that all required Primary Keys, Unique Constraints and
    Foreign Keys exist for enterprise staging tables.

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


class ConstraintValidator(BaseValidator):
    """
    Validates required database constraints.
    """

    NAME = "Database Constraints"

    REQUIRED_CONSTRAINTS = [

        # ==============================================================
        # CUSTOMER
        # ==============================================================

        ("staging", "customer", "pk_staging_customer"),
        ("staging", "customer", "fk_customer_source_system"),
        ("staging", "customer", "fk_customer_validation_status"),
        ("staging", "customer", "fk_customer_record_status"),
        ("staging", "customer", "fk_customer_etl_version"),

        # ==============================================================
        # PRODUCT
        # ==============================================================

        ("staging", "product", "pk_staging_product"),
        ("staging", "product", "fk_product_source_system"),
        ("staging", "product", "fk_product_validation_status"),
        ("staging", "product", "fk_product_record_status"),
        ("staging", "product", "fk_product_etl_version"),

        # ==============================================================
        # SELLER
        # ==============================================================

        ("staging", "seller", "pk_staging_seller"),
        ("staging", "seller", "fk_seller_source_system"),
        ("staging", "seller", "fk_seller_validation_status"),
        ("staging", "seller", "fk_seller_record_status"),
        ("staging", "seller", "fk_seller_etl_version"),

        # ==============================================================
        # GEOLOCATION
        # ==============================================================

        ("staging", "geolocation", "pk_staging_geolocation"),
        ("staging", "geolocation", "fk_geolocation_source_system"),
        ("staging", "geolocation", "fk_geolocation_validation_status"),
        ("staging", "geolocation", "fk_geolocation_record_status"),
        ("staging", "geolocation", "fk_geolocation_etl_version"),

        # ==============================================================
        # CATEGORY TRANSLATION
        # ==============================================================

        ("staging", "product_category_translation", "pk_staging_category_translation"),
        ("staging", "product_category_translation", "fk_category_translation_source_system"),
        ("staging", "product_category_translation", "fk_category_translation_validation_status"),
        ("staging", "product_category_translation", "fk_category_translation_record_status"),
        ("staging", "product_category_translation", "fk_category_translation_etl_version"),

        # ==============================================================
        # SALES ORDER
        # ==============================================================

        ("staging", "sales_order", "pk_staging_sales_order"),
        ("staging", "sales_order", "uq_sales_order_business"),
        ("staging", "sales_order", "fk_sales_order_source_system"),
        ("staging", "sales_order", "fk_sales_order_validation"),
        ("staging", "sales_order", "fk_sales_order_record_status"),
        ("staging", "sales_order", "fk_sales_order_etl_version"),

        # ==============================================================
        # SALES ORDER ITEM
        # ==============================================================

        ("staging", "sales_order_item", "pk_staging_sales_order_item"),
        ("staging", "sales_order_item", "uq_sales_order_item_business"),
        ("staging", "sales_order_item", "fk_soi_source_system"),
        ("staging", "sales_order_item", "fk_soi_validation"),
        ("staging", "sales_order_item", "fk_soi_record_status"),
        ("staging", "sales_order_item", "fk_soi_etl_version"),

        # ==============================================================
        # SALES ORDER PAYMENT
        # ==============================================================

        ("staging", "sales_order_payment", "pk_staging_sales_order_payment"),
        ("staging", "sales_order_payment", "uq_sales_order_payment_business"),
        ("staging", "sales_order_payment", "fk_sop_source_system"),
        ("staging", "sales_order_payment", "fk_sop_validation"),
        ("staging", "sales_order_payment", "fk_sop_record_status"),
        ("staging", "sales_order_payment", "fk_sop_etl_version"),

        # ==============================================================
        # SALES ORDER REVIEW
        # ==============================================================

        ("staging", "sales_order_review", "pk_staging_sales_order_review"),
        ("staging", "sales_order_review", "uq_sales_order_review_business"),
        ("staging", "sales_order_review", "fk_sor_source_system"),
        ("staging", "sales_order_review", "fk_sor_validation"),
        ("staging", "sales_order_review", "fk_sor_record_status"),
        ("staging", "sales_order_review", "fk_sor_etl_version"),
        ("staging", "sales_order_review", "chk_review_score"),

    ]

    # ------------------------------------------------------------------

    def validate(self):

        try:

            missing = []

            for schema, table, constraint in self.REQUIRED_CONSTRAINTS:

                if not self.constraint_exists(
                    schema,
                    table,
                    constraint,
                ):
                    missing.append(constraint)

            if missing:

                return self.failure(
                    self.NAME,
                    "Missing constraints: "
                    + ", ".join(missing)
                )

            return self.success(
                self.NAME,
                f"Validated {len(self.REQUIRED_CONSTRAINTS)} constraints."
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

    validator = ConstraintValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("CONSTRAINT VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)