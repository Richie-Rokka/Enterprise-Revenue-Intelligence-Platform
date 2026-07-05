"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Service Container Integration Test

Purpose
-------
Tests the Enterprise Service Container.

Author
------
ERIP

Version
-------
2.2.0
===============================================================================
"""

from __future__ import annotations

from pprint import pprint

from src.core.services import ServiceContainer


def main() -> None:

    services = ServiceContainer()

    print("=" * 70)
    print("Enterprise Service Container")
    print("=" * 70)
    print()

    # ------------------------------------------------------------------
    # Core Services
    # ------------------------------------------------------------------

    print("Initializing Core Services...")
    print()

    print("Configuration")
    print(services.config)
    print()

    print("Logger")
    print(services.logger)
    print()

    print("Database Engine")
    print(services.engine)
    print()

    print("Database Executor")
    print(services.database_executor)
    print()

    # ------------------------------------------------------------------
    # Warehouse
    # ------------------------------------------------------------------

    print("=" * 70)
    print("Warehouse Framework")
    print("=" * 70)

    print()

    print("Warehouse Manager")
    print(services.warehouse_manager)

    print()

    print("Warehouse Validator")
    print(services.warehouse_validator)

    # ------------------------------------------------------------------
    # Semantic
    # ------------------------------------------------------------------

    print()

    print("=" * 70)
    print("Semantic Framework")
    print("=" * 70)

    print()

    print("Semantic Manager")
    print(services.semantic_manager)

    print()

    print("Semantic Validator")
    print(services.semantic_validator)

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    print()

    print("=" * 70)
    print("Service Summary")
    print("=" * 70)

    pprint(services.summary())

    print()

    print("=" * 70)
    print("Service Container Test Completed Successfully")
    print("=" * 70)


if __name__ == "__main__":

    main()