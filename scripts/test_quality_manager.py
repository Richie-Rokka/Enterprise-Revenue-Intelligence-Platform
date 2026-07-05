"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : test_quality_manager.py
Purpose     : Enterprise Data Quality Framework Test
Author      : ERIP
Version     : 2.0.0

===============================================================================
"""

from pprint import pprint

from src.quality.manager import QualityManager


def main() -> None:

    manager = QualityManager()

    print("=" * 70)
    print("Enterprise Data Quality Framework")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Framework Status
    # -------------------------------------------------------------------------

    print("\nQuality Status")
    print("-" * 70)

    print(manager.status())

    # -------------------------------------------------------------------------
    # Framework Validation
    # -------------------------------------------------------------------------

    print("\nQuality Validation")
    print("-" * 70)

    pprint(manager.validate())

    # -------------------------------------------------------------------------
    # Quality Summary
    # -------------------------------------------------------------------------

    print("\nQuality Summary")
    print("-" * 70)

    pprint(manager.summary())

    # -------------------------------------------------------------------------
    # Business Rules
    # -------------------------------------------------------------------------

    print("\nBusiness Rules")
    print("-" * 70)

    pprint(manager.rules())

    # -------------------------------------------------------------------------
    # Quality Scorecard
    # -------------------------------------------------------------------------

    print("\nQuality Scorecard")
    print("-" * 70)

    pprint(manager.scorecard())

    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    print("\nQuality Dashboard")
    print("-" * 70)

    pprint(manager.dashboard())

    # -------------------------------------------------------------------------
    # Framework Version
    # -------------------------------------------------------------------------

    print("\nQuality Framework Version")
    print("-" * 70)

    print(manager.version())

    print("\n" + "=" * 70)
    print("Quality Framework Test Completed Successfully")
    print("=" * 70)


if __name__ == "__main__":

    main()