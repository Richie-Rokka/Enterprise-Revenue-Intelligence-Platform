"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : test_runtime_manager.py
Purpose     : Runtime Framework Integration Test

Author      : ERIP
Version     : 4.0.0

Description
-----------
Integration test for the Enterprise Runtime Framework.

Exercises:

- Runtime Status
- Begin Execution
- State Transition
- Runtime Metrics
- Successful Completion
- Runtime Presentation
- Framework Version

===============================================================================
"""

from __future__ import annotations

from src.core.services import ServiceContainer

from src.presentation import RuntimePresenter

from src.runtime.models import FrameworkState


def main() -> None:
    """
    Execute Runtime Framework integration test.
    """

    services = ServiceContainer()

    runtime = services.runtime_manager

    print("=" * 80)
    print("Enterprise Runtime Framework")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Runtime Status
    # -------------------------------------------------------------------------

    print("\nRuntime Status")
    print("-" * 80)

    print(

        runtime.status()

    )

    # -------------------------------------------------------------------------
    # Begin Execution
    # -------------------------------------------------------------------------

    print("\nBegin Execution")
    print("-" * 80)

    runtime.begin(

        framework="Warehouse",

        operation="Deploy",

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Update State
    # -------------------------------------------------------------------------

    print("\nUpdate State")
    print("-" * 80)

    runtime.state(

        FrameworkState.DEPLOYING

    )

    runtime.add_rows_processed(

        112650

    )

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Complete Execution
    # -------------------------------------------------------------------------

    print("\nComplete Execution")
    print("-" * 80)

    runtime.success()

    RuntimePresenter.present(

        runtime.execution

    )

    # -------------------------------------------------------------------------
    # Runtime Status
    # -------------------------------------------------------------------------

    print("\nRuntime Status")
    print("-" * 80)

    print(

        runtime.status()

    )

    # -------------------------------------------------------------------------
    # Framework Version
    # -------------------------------------------------------------------------

    print("\nRuntime Framework Version")
    print("-" * 80)

    print(

        runtime.version()

    )

    print()
    print("=" * 80)
    print("Runtime Framework Test Completed Successfully")
    print("=" * 80)


if __name__ == "__main__":

    main()