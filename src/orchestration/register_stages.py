"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : register_stages.py
Package     : src.orchestration
Purpose     : Register all platform stages
Author      : ERIP
Version     : 2.0.0
===============================================================================
"""

from src.orchestration.stage_registry import StageRegistry

from src.orchestration.stages.warehouse_stage import WarehouseStage
from src.orchestration.stages.semantic_stage import SemanticStage


def register_stages() -> None:
    """
    Register all platform stages.
    """

    # Clear previous registrations (safe for repeated runs)
    StageRegistry.clear()

    StageRegistry.register(
        WarehouseStage.name,
        WarehouseStage,
    )

    StageRegistry.register(
        SemanticStage.name,
        SemanticStage,
    )