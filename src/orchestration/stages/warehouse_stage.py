"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : warehouse_stage.py
Package     : src.orchestration.stages
Purpose     : Warehouse Stage Adapter
Author      : ERIP
Version     : 2.0.0

Description
-----------
Pipeline adapter for the Enterprise Warehouse Manager.

This class allows the Pipeline Engine to execute the existing warehouse
framework without modifying the Warehouse Manager itself.

===============================================================================
"""

from __future__ import annotations

from src.orchestration.stage import Stage
from src.orchestration.execution_context import ExecutionContext
from src.orchestration.stage_result import (
    StageResult,
    StageStatus
)

from src.warehouse.manager import WarehouseManager


class WarehouseStage(Stage):
    """
    Pipeline adapter for warehouse deployment.
    """

    name = "warehouse"

    description = "Build Enterprise Data Warehouse"

    def __init__(self) -> None:

        self.manager = WarehouseManager()

    def execute(
        self,
        context: ExecutionContext
    ) -> StageResult:

        deployment = self.manager.rebuild()

        result = StageResult(
            stage_name=self.name,
            status=(
                StageStatus.SUCCESS
                if deployment.success
                else StageStatus.FAILED
            ),
            rows_processed=deployment.scripts_executed,
            rows_loaded=deployment.scripts_executed,
            message=(
                "Warehouse deployment completed successfully."
                if deployment.success
                else "Warehouse deployment failed."
            ),
        )

        result.add_metadata(
            "validation_passed",
            deployment.validation_passed
        )

        result.add_metadata(
            "scripts_executed",
            deployment.scripts_executed
        )

        result.add_metadata(
            "warehouse_status",
            self.manager.status()
        )

        return result