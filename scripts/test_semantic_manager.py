"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Semantic Manager Integration Test

Purpose
-------
Tests the complete Semantic Framework.

Author
------
ERIP

Version
-------
2.1.0
===============================================================================
"""

from __future__ import annotations

from src.core.services import ServiceContainer

services = ServiceContainer()


def main() -> None:

    semantic = services.semantic_manager

    print("=" * 60)
    print("Semantic Layer Status")
    print("=" * 60)

    print(semantic.status())
    print()

    print("=" * 60)
    print("Semantic Layer Deployment")
    print("=" * 60)

    deployment = semantic.deploy()

    print(deployment)
    print()

    print("=" * 60)
    print("Semantic Layer Validation")
    print("=" * 60)

    validation = semantic.validate()

    print(validation)
    print()

    print("=" * 60)
    print("Semantic Layer Refresh")
    print("=" * 60)

    refresh = semantic.refresh()

    print(refresh)
    print()

    print("=" * 60)
    print("Semantic Framework Version")
    print("=" * 60)

    print(semantic.version())
    print()

    print("=" * 60)
    print("Semantic Framework Test Complete")
    print("=" * 60)


if __name__ == "__main__":

    main()