"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : test_warehouse_manager.py
Purpose     : Warehouse Framework Integration Test

Author      : ERIP
Version     : 4.0.0

Description
-----------
Integration test for the Enterprise Warehouse Framework.

Exercises:

- Framework Status
- Warehouse Deployment
- Warehouse Validation
- Warehouse Load
- Metadata Refresh
- Health Check
- Statistics
- Warehouse Refresh
- Runtime Integration
- Presentation Framework

===============================================================================
"""

from __future__ import annotations

from src.core.services import ServiceContainer

from src.presentation import (
    RuntimePresenter,
    WarehousePresenter,
)


def main() -> None:
    """
    Execute Warehouse Framework integration test.
    """

    services = ServiceContainer()

    warehouse = services.warehouse_manager
    runtime = services.runtime_manager

    print("=" * 80)
    print("Enterprise Warehouse Framework")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    print("\nWarehouse Status")
    print("-" * 80)

    print(

        warehouse.status()

    )

    # -------------------------------------------------------------------------
    # Warehouse Deployment
    # -------------------------------------------------------------------------

    print("\nWarehouse Deployment")
    print("-" * 80)

    deployment = warehouse.rebuild()

    WarehousePresenter.present(

        deployment

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Warehouse Validation
    # -------------------------------------------------------------------------

    print("\nWarehouse Validation")
    print("-" * 80)

    WarehousePresenter.present(

        warehouse.validate()

    )

    # -------------------------------------------------------------------------
    # Warehouse Load
    # -------------------------------------------------------------------------

    print("\nWarehouse Load")
    print("-" * 80)

    load = warehouse.load()

    WarehousePresenter.present(

        load

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Refresh Metadata
    # -------------------------------------------------------------------------

    print("\nRefresh Metadata")
    print("-" * 80)

    operation = warehouse.refresh_metadata()

    WarehousePresenter.present(

        operation

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Warehouse Health
    # -------------------------------------------------------------------------

    print("\nWarehouse Health")
    print("-" * 80)

    operation = warehouse.health()

    WarehousePresenter.present(

        operation

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Warehouse Statistics
    # -------------------------------------------------------------------------

    print("\nWarehouse Statistics")
    print("-" * 80)

    operation = warehouse.statistics()

    WarehousePresenter.present(

        operation

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Warehouse Refresh
    # -------------------------------------------------------------------------

    print("\nWarehouse Refresh")
    print("-" * 80)

    operation = warehouse.refresh()

    WarehousePresenter.present(

        operation

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Final Validation
    # -------------------------------------------------------------------------

    print("\nFinal Warehouse Validation")
    print("-" * 80)

    WarehousePresenter.present(

        warehouse.validate()

    )

    # -------------------------------------------------------------------------
    # Framework Version
    # -------------------------------------------------------------------------

    print("\nWarehouse Framework Version")
    print("-" * 80)

    print(

        warehouse.version()

    )

    print()
    print("=" * 80)
    print("Warehouse Framework Test Completed Successfully")
    print("=" * 80)


if __name__ == "__main__":

    main()