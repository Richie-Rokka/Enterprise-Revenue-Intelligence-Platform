"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : test_monitoring_manager.py
Purpose     : Monitoring Framework Integration Test

Author      : ERIP
Version     : 4.0.0

Description
-----------
Integration test for the Enterprise Monitoring Framework.

Exercises

- Framework Status
- Platform Health
- Runtime Metrics
- Monitoring Statistics
- Enterprise Dashboard
- Monitoring Validation
- Runtime Integration
- Framework Version

===============================================================================
"""

from __future__ import annotations

from src.core.services import ServiceContainer

from src.presentation import (
    MonitoringPresenter,
    RuntimePresenter,
)


def main() -> None:
    """
    Execute Monitoring Framework integration test.
    """

    services = ServiceContainer()

    monitoring = services.monitoring_manager
    runtime = services.runtime_manager

    print("=" * 80)
    print("Enterprise Monitoring Framework")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    print("\nMonitoring Status")
    print("-" * 80)

    print(

        monitoring.status()

    )

    # -------------------------------------------------------------------------
    # Platform Health
    # -------------------------------------------------------------------------

    print("\nPlatform Health")
    print("-" * 80)

    MonitoringPresenter.present(

        monitoring.health()

    )

    # -------------------------------------------------------------------------
    # Runtime Metrics
    # -------------------------------------------------------------------------

    print("\nRuntime Metrics")
    print("-" * 80)

    MonitoringPresenter.present(

        monitoring.metrics()

    )

    # -------------------------------------------------------------------------
    # Monitoring Statistics
    # -------------------------------------------------------------------------

    print("\nMonitoring Statistics")
    print("-" * 80)

    operation = monitoring.statistics()

    MonitoringPresenter.present(

        operation

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Enterprise Dashboard
    # -------------------------------------------------------------------------

    print("\nEnterprise Monitoring Dashboard")
    print("-" * 80)

    MonitoringPresenter.present(

        monitoring.dashboard()

    )

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    print("\nMonitoring Validation")
    print("-" * 80)

    MonitoringPresenter.present(

        monitoring.validate()

    )

    # -------------------------------------------------------------------------
    # Final Validation
    # -------------------------------------------------------------------------

    print("\nFinal Monitoring Validation")
    print("-" * 80)

    MonitoringPresenter.present(

        monitoring.validate()

    )

    # -------------------------------------------------------------------------
    # Framework Version
    # -------------------------------------------------------------------------

    print("\nMonitoring Framework Version")
    print("-" * 80)

    print(

        monitoring.version()

    )

    print()

    print("=" * 80)
    print("Monitoring Framework Test Completed Successfully")
    print("=" * 80)


if __name__ == "__main__":

    main()