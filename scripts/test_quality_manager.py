"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : test_quality_manager.py
Purpose     : Enterprise Data Quality Framework Integration Test

Author      : ERIP
Version     : 3.0.0

Description
-----------
Integration test for the Enterprise Data Quality Framework.

Exercises

- Framework Status
- Framework Validation
- Quality Summary
- Business Rules
- Quality Scorecard
- Enterprise Dashboard
- Framework Version

===============================================================================
"""

from __future__ import annotations

from src.core.services import ServiceContainer

from src.presentation import (
    QualityPresenter,
)


def main() -> None:
    """
    Execute Enterprise Data Quality Framework integration test.
    """

    services = ServiceContainer()

    quality = services.quality_manager

    print("=" * 80)
    print("Enterprise Data Quality Framework")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Framework Status
    # -------------------------------------------------------------------------

    print("\nQuality Status")
    print("-" * 80)

    print(

        quality.status()

    )

    # -------------------------------------------------------------------------
    # Framework Validation
    # -------------------------------------------------------------------------

    print("\nQuality Validation")
    print("-" * 80)

    QualityPresenter.present(

        quality.validate()

    )

    # -------------------------------------------------------------------------
    # Quality Summary
    # -------------------------------------------------------------------------

    print("\nQuality Summary")
    print("-" * 80)

    QualityPresenter.present(

        quality.summary()

    )

    # -------------------------------------------------------------------------
    # Business Rules
    # -------------------------------------------------------------------------

    print("\nBusiness Rules")
    print("-" * 80)

    QualityPresenter.present(

        quality.rules()

    )

    # -------------------------------------------------------------------------
    # Quality Scorecard
    # -------------------------------------------------------------------------

    print("\nQuality Scorecard")
    print("-" * 80)

    QualityPresenter.present(

        quality.scorecard()

    )

    # -------------------------------------------------------------------------
    # Enterprise Dashboard
    # -------------------------------------------------------------------------

    print("\nQuality Dashboard")
    print("-" * 80)

    QualityPresenter.present(

        quality.dashboard()

    )

    # -------------------------------------------------------------------------
    # Final Validation
    # -------------------------------------------------------------------------

    print("\nFinal Quality Validation")
    print("-" * 80)

    QualityPresenter.present(

        quality.validate()

    )

    # -------------------------------------------------------------------------
    # Framework Version
    # -------------------------------------------------------------------------

    print("\nQuality Framework Version")
    print("-" * 80)

    print(

        quality.version()

    )

    print()
    print("=" * 80)
    print("Quality Framework Test Completed Successfully")
    print("=" * 80)


if __name__ == "__main__":

    main()