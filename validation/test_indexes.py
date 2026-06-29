"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    test_indexes.py

Purpose:
    Validate database indexes for the ERIP warehouse.

Description:
    Verifies that all required indexes exist for enterprise staging tables.

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


class IndexValidator(BaseValidator):
    """
    Validates required database indexes.
    """

    NAME = "Database Indexes"

    REQUIRED_INDEXES = [

        # ==============================================================
        # CUSTOMER
        # ==============================================================

        "idx_customer_business_key",
        "idx_customer_unique",
        "idx_customer_batch",
        "idx_customer_load",
        "idx_customer_source",
        "idx_customer_source_file",
        "idx_customer_hash",
        "idx_customer_ingested",
        "idx_customer_validation",
        "idx_customer_record_status",

        # ==============================================================
        # PRODUCT
        # ==============================================================

        "idx_product_business_key",
        "idx_product_category",
        "idx_product_batch",
        "idx_product_load",
        "idx_product_source",
        "idx_product_source_file",
        "idx_product_hash",
        "idx_product_ingested",
        "idx_product_validation",
        "idx_product_record_status",

        # ==============================================================
        # SELLER
        # ==============================================================

        "idx_seller_business_key",
        "idx_seller_city",
        "idx_seller_state",
        "idx_seller_batch",
        "idx_seller_load",
        "idx_seller_source",
        "idx_seller_source_file",
        "idx_seller_hash",
        "idx_seller_ingested",
        "idx_seller_validation",
        "idx_seller_record_status",

        # ==============================================================
        # GEOLOCATION
        # ==============================================================

        "idx_geolocation_zip",
        "idx_geolocation_city",
        "idx_geolocation_state",
        "idx_geolocation_coordinates",
        "idx_geolocation_batch",
        "idx_geolocation_load",
        "idx_geolocation_source",
        "idx_geolocation_ingested",
        "idx_geolocation_hash",
        "idx_geolocation_validation",
        "idx_geolocation_record_status",

        # ==============================================================
        # PRODUCT CATEGORY TRANSLATION
        # ==============================================================

        "idx_category_name",
        "idx_category_name_english",
        "idx_category_batch",
        "idx_category_load",
        "idx_category_source",
        "idx_category_source_file",
        "idx_category_ingested",
        "idx_category_hash",
        "idx_category_validation",
        "idx_category_record_status",

        # ==============================================================
        # SALES ORDER
        # ==============================================================

        "idx_sales_order_customer",
        "idx_sales_order_status",
        "idx_sales_order_purchase_date",
        "idx_sales_order_estimated_delivery",
        "idx_sales_order_batch",
        "idx_sales_order_load",
        "idx_sales_order_source",
        "idx_sales_order_source_file",
        "idx_sales_order_ingested",
        "idx_sales_order_hash",
        "idx_sales_order_validation",
        "idx_sales_order_record_status",

        # ==============================================================
        # SALES ORDER ITEM
        # ==============================================================

        "idx_soi_order",
        "idx_soi_product",
        "idx_soi_seller",
        "idx_soi_shipping_date",
        "idx_soi_price",
        "idx_soi_freight",
        "idx_soi_batch",
        "idx_soi_load",
        "idx_soi_source",
        "idx_soi_ingested",
        "idx_soi_hash",
        "idx_soi_validation",
        "idx_soi_record_status",

        # ==============================================================
        # SALES ORDER PAYMENT
        # ==============================================================

        "idx_sop_order",
        "idx_sop_payment_type",
        "idx_sop_installments",
        "idx_sop_payment_value",
        "idx_sop_batch",
        "idx_sop_load",
        "idx_sop_source",
        "idx_sop_source_file",
        "idx_sop_ingested",
        "idx_sop_hash",
        "idx_sop_validation",
        "idx_sop_record_status",

        # ==============================================================
        # SALES ORDER REVIEW
        # ==============================================================

        "idx_sor_review_id",
        "idx_sor_order",
        "idx_sor_score",
        "idx_sor_creation_date",
        "idx_sor_batch",
        "idx_sor_load",
        "idx_sor_source",
        "idx_sor_source_file",
        "idx_sor_ingested",
        "idx_sor_hash",
        "idx_sor_validation",
        "idx_sor_record_status",

    ]

    # -----------------------------------------------------------------

    def validate(self):

        try:

            missing = []

            for index in self.REQUIRED_INDEXES:

                if not self.index_exists(index):

                    missing.append(index)

            if missing:

                return self.failure(
                    self.NAME,
                    "Missing indexes: "
                    + ", ".join(missing)
                )

            return self.success(
                self.NAME,
                f"Validated {len(self.REQUIRED_INDEXES)} indexes."
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

    validator = IndexValidator()

    result = validator.validate()

    print()

    print("=" * 70)

    print("INDEX VALIDATION")

    print("=" * 70)

    print()

    print(f"Validator : {result.name}")

    print(f"Status    : {'PASS' if result.passed else 'FAIL'}")

    print(f"Message   : {result.message}")

    print()

    print("=" * 70)