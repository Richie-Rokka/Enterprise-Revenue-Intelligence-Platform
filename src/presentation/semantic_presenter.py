"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : semantic_presenter.py
Package     : src.presentation
Purpose     : Enterprise Semantic Layer Presenter

Author      : ERIP
Version     : 3.0.0

Description
-----------
Enterprise presenter for the Semantic Framework.

Renders Semantic Framework models using the Enterprise Presentation
Framework.

===============================================================================
"""

from __future__ import annotations

from src.database.database_executor import ExecutionResult

from src.presentation.base_presenter import BasePresenter
from src.presentation.console import Console
from src.presentation.formatter import Formatter
from src.presentation.report import Report

from src.semantic.manager import (
    SemanticDeploymentResult,
)

from src.semantic.validator import (
    ValidationResult,
)


# =============================================================================
# Semantic Presenter
# =============================================================================


class SemanticPresenter(BasePresenter):
    """
    Enterprise Semantic Presenter.
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
        Render a Semantic presentation model.
        """

        if isinstance(
            model,
            SemanticDeploymentResult,
        ):

            return cls._deployment(
                model
            )

        if isinstance(
            model,
            ValidationResult,
        ):

            return cls._validation(
                model
            )

        if isinstance(
            model,
            ExecutionResult,
        ):

            return cls._operation(
                model
            )

        raise TypeError(

            f"Unsupported Semantic presentation model: "

            f"{type(model).__name__}"

        )

    # -------------------------------------------------------------------------
    # Deployment
    # -------------------------------------------------------------------------

    @classmethod
    def _deployment(
        cls,
        result: SemanticDeploymentResult,
    ) -> str:
        """
        Render Semantic deployment summary.
        """

        report = Report(

            "Semantic Deployment Summary"

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

                status=(
                    "PASSED"
                    if result.validation_result.passed
                    else "FAILED"
                ),

                checks=result.validation_result.checks_performed,

                failures=len(

                    result.validation_result.failures

                ),

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
        Render Semantic validation summary.
        """

        report = Report(

            "Semantic Validation Summary"

        )

        report.add_section(

            title="Validation",

            body=Console.key_values(

                status=(
                    "PASSED"
                    if result.passed
                    else "FAILED"
                ),

                checks_performed=result.checks_performed,

                failures=len(

                    result.failures

                ),

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
        Render Semantic operation summary.
        """

        report = Report(

            "Semantic Operation Summary"

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