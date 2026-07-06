"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : test_monitoring_manager.py
Purpose     : Monitoring Framework Test
Author      : ERIP
Version     : 2.0.0

===============================================================================
"""

from pprint import pprint

from src.core.services import ServiceContainer

services = ServiceContainer()


def main() -> None:

    manager = services.monitoring_manager

    print("=" * 70)
    print("Enterprise Monitoring Framework")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Framework Status
    # -------------------------------------------------------------------------

    print("\nMonitoring Status")
    print("-" * 70)

    print(manager.status())

    # -------------------------------------------------------------------------
    # Platform Health
    # -------------------------------------------------------------------------

    print("\nPlatform Health")
    print("-" * 70)

    pprint(manager.health())

    # -------------------------------------------------------------------------
    # Runtime Metrics
    # -------------------------------------------------------------------------

    print("\nRuntime Metrics")
    print("-" * 70)

    pprint(manager.metrics())

    # -------------------------------------------------------------------------
    # Warehouse Statistics
    # -------------------------------------------------------------------------

    print("\nWarehouse Statistics")
    print("-" * 70)

    pprint(manager.warehouse_statistics())

    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    print("\nMonitoring Dashboard")
    print("-" * 70)

    pprint(manager.dashboard())

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    print("\nMonitoring Validation")
    print("-" * 70)

    pprint(manager.validate())

    # -------------------------------------------------------------------------
    # Version
    # -------------------------------------------------------------------------

    print("\nMonitoring Framework Version")
    print("-" * 70)

    print(manager.version())

    print("\n" + "=" * 70)
    print("Monitoring Framework Test Completed Successfully")
    print("=" * 70)


if __name__ == "__main__":

    main()