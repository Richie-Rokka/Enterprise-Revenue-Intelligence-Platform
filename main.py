"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : main.py
Purpose     : Enterprise Platform Entry Point
Author      : ERIP
Version     : 3.0.0

Description
-----------
Application entry point for the Enterprise Revenue Intelligence Platform.

Responsibilities
----------------
• Bootstrap the Enterprise Platform
• Initialize platform services
• Perform platform health checks
• Execute the enterprise pipeline
• Shutdown platform gracefully
• Return appropriate process exit codes

Notes
-----
This module intentionally contains no business logic.

All orchestration is delegated to the Platform class.

===============================================================================
"""

from __future__ import annotations

import sys

from src.core.platform import Platform


# =============================================================================
# Main
# =============================================================================


def main() -> int:
    """
    Execute the Enterprise Revenue Intelligence Platform.

    Returns
    -------
    int
        Process exit code.
    """

    platform = Platform()

    try:

        # -----------------------------------------------------------------
        # Platform Initialization
        # -----------------------------------------------------------------

        platform.initialize()

        # -----------------------------------------------------------------
        # Platform Health Check
        # -----------------------------------------------------------------

        health = platform.health()

        if health.overall != "HEALTHY":

            print()

            print("Platform health check failed.")

            print()

            print(health)

            return 2

        # -----------------------------------------------------------------
        # Execute Enterprise Platform
        # -----------------------------------------------------------------

        platform.run()

        return 0

    except KeyboardInterrupt:

        print()

        print("Platform execution cancelled by user.")

        return 130

    except Exception as error:

        print()

        print(f"Platform execution failed: {error}")

        return 1

    finally:

        try:

            platform.shutdown()

        except Exception:

            pass


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":

    sys.exit(main())