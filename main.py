"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : main.py
Purpose     : Enterprise Platform Entry Point
Author      : ERIP
Version     : 3.1.0

Description
-----------
Application entry point for the Enterprise Revenue Intelligence Platform.

Responsibilities
----------------
• Bootstrap the Enterprise Platform
• Initialize platform services
• Execute the Enterprise Pipeline
• Perform post-execution health checks
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
        # Execute Enterprise Platform
        # -----------------------------------------------------------------

        platform.run()

        # -----------------------------------------------------------------
        # Post-Execution Health Check
        # -----------------------------------------------------------------

        health = platform.health()

        print()
        print("=" * 70)
        print("Enterprise Platform Health")
        print("=" * 70)
        print(health)
        print()

        if health.overall != "HEALTHY":

            print("WARNING: Platform completed but health is UNHEALTHY.")

            return 2

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