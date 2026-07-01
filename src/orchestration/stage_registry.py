"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : stage_registry.py
Package     : src.orchestration
Purpose     : Central registry for pipeline stages
Author      : ERIP
Version     : 2.0.0

Description
-----------
Provides a centralized registry used by the Pipeline Engine to resolve
configured stage names into executable Stage implementations.

===============================================================================
"""

from __future__ import annotations

from typing import Type

from src.orchestration.stage import Stage


class StageRegistry:
    """
    Registry of available pipeline stages.
    """

    _registry: dict[str, Type[Stage]] = {}

    @classmethod
    def register(
        cls,
        stage_name: str,
        stage_class: Type[Stage]
    ) -> None:
        """
        Register a stage.
        """

        cls._registry[stage_name] = stage_class

    @classmethod
    def get(
        cls,
        stage_name: str
    ) -> Stage:
        """
        Resolve a stage instance.
        """

        if stage_name not in cls._registry:

            raise KeyError(
                f"Unknown pipeline stage: {stage_name}"
            )

        return cls._registry[stage_name]()

    @classmethod
    def registered_stages(cls) -> list[str]:
        """
        Return registered stage names.
        """

        return sorted(cls._registry.keys())

    @classmethod
    def exists(
        cls,
        stage_name: str
    ) -> bool:
        """
        Returns True if a stage is registered.
        """

        return stage_name in cls._registry

    @classmethod
    def clear(cls) -> None:
        """
        Clear registry.
        """

        cls._registry.clear()