"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : quality_presenter.py
Package     : src.presentation
Purpose     : Enterprise Data Quality Presenter

Author      : ERIP
Version     : 2.0.0

Description
-----------
Enterprise presenter for the Data Quality Framework.

Renders Data Quality Framework models using the Enterprise Presentation
Framework.

===============================================================================
"""

from __future__ import annotations

from src.presentation.base_presenter import BasePresenter
from src.presentation.console import Console
from src.presentation.formatter import Formatter
from src.presentation.report import Report

from src.quality.models import (
    BusinessRuleSummary,
    DataQualityValidationResult,
    QualityDashboard,
    QualityScorecard,
    QualitySummary,
)


# =============================================================================
# Quality Presenter
# =============================================================================


class QualityPresenter(BasePresenter):
    """
    Enterprise Data Quality Presenter.
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
        Render a Data Quality presentation model.
        """

        if isinstance(
            model,
            DataQualityValidationResult,
        ):

            return cls._validation(
                model
            )

        if isinstance(
            model,
            QualitySummary,
        ):

            return cls._summary(
                model
            )

        if isinstance(
            model,
            QualityScorecard,
        ):

            return cls._scorecard(
                model
            )

        if isinstance(
            model,
            BusinessRuleSummary,
        ):

            return cls._rules(
                model
            )

        if isinstance(
            model,
            QualityDashboard,
        ):

            return cls._dashboard(
                model
            )

        raise TypeError(

            f"Unsupported Quality presentation model: "

            f"{type(model).__name__}"

        )

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    @classmethod
    def _validation(
        cls,
        result: DataQualityValidationResult,
    ) -> str:
        """
        Render Data Quality validation summary.
        """

        report = Report(

            "Data Quality Validation Summary"

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
    # Quality Summary
    # -------------------------------------------------------------------------

    @classmethod
    def _summary(
        cls,
        result: QualitySummary,
    ) -> str:
        """
        Render enterprise quality summary.
        """

        report = Report(

            "Enterprise Quality Summary"

        )

        report.add_section(

            title="Execution Summary",

            body=Console.key_values(

                total_rules=result.total_rules,

                rules_passed=result.rules_passed,

                rules_failed=result.rules_failed,

                total_rows_checked=result.total_rows_checked,

                total_rows_failed=result.total_rows_failed,

                execution_time=Formatter.duration(

                    result.execution_time_seconds

                ),

            ),

        )

        return report.build()

    # -------------------------------------------------------------------------
    # Quality Scorecard
    # -------------------------------------------------------------------------

    @classmethod
    def _scorecard(
        cls,
        result: QualityScorecard,
    ) -> str:
        """
        Render enterprise quality scorecard.
        """

        report = Report(

            "Enterprise Quality Scorecard"

        )

        report.add_section(

            title="Quality Scores",

            body=Console.key_values(

                completeness=f"{result.completeness_score:.1f}%",

                uniqueness=f"{result.uniqueness_score:.1f}%",

                consistency=f"{result.consistency_score:.1f}%",

                referential_integrity=f"{result.referential_integrity_score:.1f}%",

                freshness=f"{result.freshness_score:.1f}%",

                overall_score=f"{result.overall_score:.1f}%",

                grade=result.grade,

            ),

        )

        return report.build()

    # -------------------------------------------------------------------------
    # Business Rules
    # -------------------------------------------------------------------------

    @classmethod
    def _rules(
        cls,
        result: BusinessRuleSummary,
    ) -> str:
        """
        Render business rule execution summary.
        """

        report = Report(

            "Business Rule Summary"

        )

        report.add_section(

            title="Business Rules",

            body=Console.key_values(

                rules_executed=result.rules_executed,

                rules_passed=result.rules_passed,

                rules_failed=result.rules_failed,

                critical_failures=result.critical_failures,

                warning_failures=result.warning_failures,

            ),

        )

        return report.build()

    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    @classmethod
    def _dashboard(
        cls,
        result: QualityDashboard,
    ) -> str:
        """
        Render Enterprise Quality Dashboard.
        """

        report = Report(

            "Enterprise Quality Dashboard"

        )

        report.add_section(

            title="Validation",

            body=Console.key_values(

                status=(

                    "PASSED"

                    if result.validation.passed

                    else "FAILED"

                ),

                checks_performed=result.validation.checks_performed,

                failures=len(

                    result.validation.failures

                ),

            ),

        )

        report.add_section(

            title="Execution Summary",

            body=Console.key_values(

                total_rules=result.summary.total_rules,

                rules_passed=result.summary.rules_passed,

                rules_failed=result.summary.rules_failed,

                total_rows_checked=result.summary.total_rows_checked,

                total_rows_failed=result.summary.total_rows_failed,

            ),

        )

        report.add_section(

            title="Quality Scorecard",

            body=Console.key_values(

                completeness=f"{result.scorecard.completeness_score:.1f}%",

                uniqueness=f"{result.scorecard.uniqueness_score:.1f}%",

                consistency=f"{result.scorecard.consistency_score:.1f}%",

                referential_integrity=(
                    f"{result.scorecard.referential_integrity_score:.1f}%"
                ),

                freshness=f"{result.scorecard.freshness_score:.1f}%",

                overall_score=f"{result.scorecard.overall_score:.1f}%",

                grade=result.scorecard.grade,

            ),

        )

        report.add_section(

            title="Business Rules",

            body=Console.key_values(

                rules_executed=result.business_rules.rules_executed,

                rules_passed=result.business_rules.rules_passed,

                rules_failed=result.business_rules.rules_failed,

                critical_failures=result.business_rules.critical_failures,

                warning_failures=result.business_rules.warning_failures,

            ),

        )

        return report.build()