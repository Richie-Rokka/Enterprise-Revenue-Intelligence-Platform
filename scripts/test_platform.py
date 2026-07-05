"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : test_platform.py
Package     : scripts
Purpose     : Platform Integration Test
Author      : ERIP
Version     : 2.2.0

Description
-----------
Integration test for the Enterprise Platform.

Validates:
- Platform Status
- Platform Validation
- Platform Health
- Platform Deployment
- Platform Refresh
- Platform Version

===============================================================================
"""

from __future__ import annotations

from pprint import pprint

from src.core.platform import Platform


def separator(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def main() -> None:

    platform = Platform()

    # ---------------------------------------------------------------------
    # Status
    # ---------------------------------------------------------------------

    separator("Platform Status")

    print(platform.status())

    # ---------------------------------------------------------------------
    # Validation
    # ---------------------------------------------------------------------

    separator("Platform Validation")

    validation = platform.validate()

    pprint(validation)

    # ---------------------------------------------------------------------
    # Health
    # ---------------------------------------------------------------------

    separator("Platform Health")

    health = platform.health()

    pprint(health)

    # ---------------------------------------------------------------------
    # Deployment
    # ---------------------------------------------------------------------

    separator("Platform Deployment")

    deployment = platform.deploy()

    pprint(deployment)

    # ---------------------------------------------------------------------
    # Refresh
    # ---------------------------------------------------------------------

    separator("Platform Refresh")

    refresh = platform.refresh()

    pprint(refresh)

    # ---------------------------------------------------------------------
    # Version
    # ---------------------------------------------------------------------

    separator("Platform Version")

    print(platform.version())

    print()

    print("=" * 70)
    print("Platform Framework Test Complete")
    print("=" * 70)


if __name__ == "__main__":

    main()