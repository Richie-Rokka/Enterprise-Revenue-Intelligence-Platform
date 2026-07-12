"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Script      : test_customer_pipeline.py
Purpose     : Customer Pipeline Smoke Test

Description
-----------
Validates the complete Customer ETL pipeline:

    Extract
        ↓
    Transform
        ↓
    Validate
        ↓
    Load

This script is intended as a regression smoke test for the
Enterprise ETL Framework.
===============================================================================
"""

from src.etl.dataset_registry import DatasetRegistry


def main() -> None:

    DatasetRegistry.register_all()

    pipeline = DatasetRegistry.build_pipeline(
        "customer"
    )

    result = pipeline.execute()

    print("\n" + "=" * 70)
    print("CUSTOMER PIPELINE SMOKE TEST")
    print("=" * 70)
    print(f"Pipeline           : {result.pipeline_name}")
    print(f"Rows Extracted     : {result.rows_extracted:,}")
    print(f"Rows Transformed   : {result.rows_transformed:,}")
    print(f"Rows Validated     : {result.rows_validated:,}")
    print(f"Rows Loaded        : {result.load_result.rows_loaded:,}")
    print(f"Success            : {result.load_result.success}")
    print("=" * 70)


if __name__ == "__main__":
    main()