"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : warehouse_presenter.py
Package     : src.presentation
Purpose     : Enterprise Warehouse Presenter

Author      : ERIP
Version     : 3.0.0

Description
-----------
Enterprise presenter for the Warehouse Framework.

Responsible for rendering Warehouse Framework models through the
Enterprise Presentation Framework.

===============================================================================
"""

from __future__ import annotations

from src.database.database_executor import ExecutionResult

from src.presentation.base_presenter import BasePresenter
from src.presentation.console import Console
from src.presentation.formatter import Formatter
from src.presentation.report import Report

from src.warehouse.manager import (
    WarehouseDeploymentResult,
    WarehouseLoadResult,
)

from src.warehouse.validator import ValidationResult


# =============================================================================
# Warehouse Presenter
# =============================================================================


class WarehousePresenter(BasePresenter):
    """
    Enterprise Warehouse Presenter.
    """

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        model: object,
    ) -> str:
        """
        Render a Warehouse presentation model.
        """

        if isinstance(model, WarehouseDeploymentResult):

            return cls._deployment(model)

        if isinstance(model, WarehouseLoadResult):

            return cls._load(model)

        if isinstance(model, ValidationResult):

            return cls._validation(model)

        if isinstance(model, ExecutionResult):

            return cls._operation(model)

        raise TypeError(

            f"Unsupported Warehouse presentation model: "
            f"{type(model).__name__}"

        )

    # -------------------------------------------------------------------------
    # Deployment
    # -------------------------------------------------------------------------

    @classmethod
    def _deployment(
        cls,
        result: WarehouseDeploymentResult,
    ) -> str:
        """
        Render warehouse deployment summary.
        """

        report = Report(

            "Warehouse Deployment Summary"

        )

        report.add_section(

            title="Deployment",

            body=Console.key_values(

                success=Formatter.boolean(

                    result.success

                ),

                scripts_executed=result.scripts_executed,

                validation_passed=Formatter.boolean(

                    result.validation_passed

                ),

            ),

        )

        report.add_section(

            title="Validation",

            body=Console.key_values(

                status="PASSED"

                if result.validation_result.passed

                else "FAILED",

                checks=result.validation_result.checks_performed,

                failures=len(

                    result.validation_result.failures

                ),

            ),

        )

        return report.build()

    # -------------------------------------------------------------------------
    # Warehouse Load
    # -------------------------------------------------------------------------

    @classmethod
    def _load(
        cls,
        result: WarehouseLoadResult,
    ) -> str:
        """
        Render warehouse load summary.
        """

        report = Report(

            "Warehouse Load Summary"

        )

        report.add_section(

            title="Load Summary",

            body=Console.key_values(

                success=Formatter.boolean(

                    result.success

                ),

                procedures_executed=result.procedures_executed,

                execution_time=Formatter.duration(

                    result.execution_time_seconds

                ),

            ),

        )

        if result.steps:

            report.add_section(

                title="Procedures",

                body=Console.join(

                    *[

                        Console.key_value(

                            step.procedure,

                            (
                                "SUCCESS"
                                if step.success
                                else f"FAILED ({Formatter.text(step.error)})"
                            ),

                        )

                        for step in result.steps

                    ]

                ),

            )

        return report.build()

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    @classmethod
    def _validation(
        cls,
        result: ValidationResult,
    ) -> str:
        """
        Render warehouse validation results.
        """

        report = Report(

            "Warehouse Validation Summary"

        )

        report.add_section(

            title="Validation",

            body=Console.key_values(

                status="PASSED" if result.passed else "FAILED",

                checks_performed=result.checks_performed,

                failures=len(result.failures),

            ),

        )

        if result.failures:

            report.add_section(

                title="Validation Failures",

                body=Console.join(

                    *result.failures

                ),

            )

        return report.build()

    # -------------------------------------------------------------------------
    # Operation
    # -------------------------------------------------------------------------

    @classmethod
    def _operation(
        cls,
        result: ExecutionResult,
    ) -> str:
        """
        Render operational SQL execution results.
        """

        report = Report(

            "Warehouse Operation Summary"

        )

        report.add_section(

            title="Execution",

            body=Console.key_values(

                script_name=result.script_name,

                success=Formatter.boolean(

                    result.success

                ),

                execution_time=Formatter.duration(

                    result.execution_time_seconds

                ),

            ),

        )

        if result.error:

            report.add_section(

                title="Error",

                body=Formatter.text(

                    result.error

                ),

            )

        return report.build()