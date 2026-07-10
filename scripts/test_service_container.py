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

    
    print("Database Health")
    print(services.database_health.check())
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


    print()
    print("=" * 70)
    print("Monitoring Framework")
    print("=" * 70)
    print()

    print("Monitoring Manager")
    print(services.monitoring_manager)
    print()

    print("Monitoring Validator")
    print(services.monitoring_validator)

    print()
    print("=" * 70)
    print("Quality Framework")
    print("=" * 70)
    print()

    print()

    print("Quality Manager")
    print(services.quality_manager)
    print()

    print("Scorecard Engine")
    print(services.scorecard_engine)
    print()

    print("Quality Validator")
    print(services.quality_validator)

    print("=" * 70)
    print("ETL Framework")
    print("=" * 70)
    
    print()
    
    print("ETL Manager")
    
    print(services.etl_manager)

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