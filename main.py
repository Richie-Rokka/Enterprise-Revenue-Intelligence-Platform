"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : main.py
Purpose     : Application Entry Point
Author      : ERIP
Version     : 2.1.0

Description
-----------
Application entry point for the Enterprise Revenue Intelligence Platform.

Responsibilities
----------------
- Bootstrap the platform
- Execute the platform lifecycle
- Return appropriate process exit codes

Notes
-----
This module intentionally contains no business logic.
All orchestration is delegated to the Platform class.

===============================================================================
"""

from __future__ import annotations

import sys

from src.core.platform import Platform


def main() -> int:
    """
    Execute the Enterprise Revenue Intelligence Platform.

    Returns
    -------
    int
        Process exit code.
    """

    try:

        platform = Platform()

        platform.run()

        return 0

    except KeyboardInterrupt:

        print("\nPlatform execution cancelled by user.")

        return 130

    except Exception as error:

        print(f"\nPlatform execution failed: {error}")

        return 1


if __name__ == "__main__":

    sys.exit(main())