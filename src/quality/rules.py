"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : rules.py
Package     : src.quality
Purpose     : Enterprise Data Quality Rules Engine
Author      : ERIP
Version     : 2.0.0

Description
-----------
Executes Enterprise Data Quality rules.

Responsibilities
----------------
- Register quality rules
- Execute quality rules
- Return standardized quality results

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from src.database.database_executor import DatabaseExecutor

from time import perf_counter

from .registry import QualityRuleRegistry
from src.observability import get_logger

from uuid import uuid4

from sqlalchemy import text

from .models import (
    QualityCheckResult,
    QualityRule,
)


logger = get_logger(__name__)


# =============================================================================
# Rules Engine
# =============================================================================


class RulesEngine:
    """
    Enterprise Data Quality Rules Engine.
    """

    VERSION = "2.0.0"

    # -------------------------------------------------------------------------

    def __init__(
        self,
        executor: DatabaseExecutor,
    ) -> None:

        self.executor = executor

        self.registry = QualityRuleRegistry()

        self._quality_directory = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "quality"
        )

        self._register_default_rules()
    # -------------------------------------------------------------------------

    def _register_default_rules(self) -> None:
        """
        Register default enterprise quality rules.
        """

        self.registry.register(
            QualityRule(
                rule_id="DQ-001",
                name="Duplicate Customer Detection",
                description="Detect duplicate customer business keys.",
                category="Uniqueness",
                severity="CRITICAL",
                script_name="001_check_duplicate_customers.sql",
            )
        )

        self.registry.register(
            QualityRule(
                rule_id="DQ-002",
                name="Customer Name Completeness",
                description="Customer name completeness.",
                category="Completeness",
                severity="HIGH",
                script_name="002_check_null_customer_names.sql",
            )
        )

        self.registry.register(
            QualityRule(
                rule_id="DQ-003",
                name="Duplicate Product Detection",
                description="Duplicate product business keys.",
                category="Uniqueness",
                severity="CRITICAL",
                script_name="003_check_duplicate_products.sql",
            )
        )

        self.registry.register(
            QualityRule(
                rule_id="DQ-004",
                name="Orphan Fact Sales Detection",
                description="Fact table referential integrity.",
                category="Referential Integrity",
                severity="CRITICAL",
                script_name="004_check_orphan_fact_sales.sql",
            )
        )

        self.registry.register(
            QualityRule(
                rule_id="DQ-005",
                name="Negative Payment Detection",
                description="Detect negative payment values.",
                category="Business Rule",
                severity="CRITICAL",
                script_name="005_check_negative_payment.sql",
            )
        )

    # -------------------------------------------------------------------------

    @property
    def rules(self) -> list[QualityRule]:
        """
        Registered quality rules.
        """

        return self.registry.rules

    # -------------------------------------------------------------------------

    def execute(self) -> list[QualityCheckResult]:
        """
        Execute all quality rules.

        NOTE
        ----
        Placeholder implementation.

        Future versions will execute SQL assets discovered by
        QualityRegistry.
        """

        logger.info("=" * 60)
        logger.info("Executing Enterprise Data Quality Rules")
        logger.info("=" * 60)

        results: list[QualityCheckResult] = []

        for rule in self.registry.enabled_rules():

            start = perf_counter()

            script_path = self._quality_directory / rule.script_name

            execution = self.executor.execute(

                script_path=script_path,

                script_name=rule.script_name,

            )

            elapsed = perf_counter() - start

            passed = execution.success

            rows_checked = execution.rows_processed

            rows_failed = 0

            message = "Rule executed successfully."

            if execution.query_result is not None:

                passed = execution.query_result["passed"]

                rows_checked = execution.query_result["rows_checked"]

                rows_failed = execution.query_result["rows_failed"]

                message = execution.query_result["message"]

            logger.info(

                "Rule %-35s %s",

                rule.name,

                "PASS" if passed else "FAIL",

            )

            result = QualityCheckResult(

                rule_id=rule.rule_id,

                rule_name=rule.name,

                category=rule.category,

                severity=rule.severity,

                passed=passed,

                rows_checked=rows_checked,

                rows_failed=rows_failed,

                execution_time_seconds=elapsed,

                quality_score=execution.query_result["quality_score"],

                message=message,

            )

            results.append(result)

            self._save_history(result)

        logger.info("=" * 60)
        logger.info(

            "Completed %s quality rules.",

            len(results),

        )
        logger.info("=" * 60)

        return results

    # -------------------------------------------------------------------------

    def _save_history(
        self,
        result: QualityCheckResult,
    ) -> None:

        sql = """
            INSERT INTO monitoring.quality_rule_history
            (
                execution_id,
                rule_id,
                rule_name,
                category,
                severity,
                passed,
                rows_checked,
                rows_failed,
                quality_score,
                execution_time_ms,
                message
            )
            VALUES
            (
                :execution_id,
                :rule_id,
                :rule_name,
                :category,
                :severity,
                :passed,
                :rows_checked,
                :rows_failed,
                :quality_score,
                :execution_time_ms,
                :message
            )
        """

        with self.executor.engine.begin() as connection:

            connection.execute(

                text(sql),

                {
                    "execution_id": uuid4(),
                    "rule_id": result.rule_id,
                    "rule_name": result.rule_name,
                    "category": result.category,
                    "severity": result.severity,
                    "passed": result.passed,
                    "rows_checked": result.rows_checked,
                    "rows_failed": result.rows_failed,
                    "quality_score": result.quality_score,
                    "execution_time_ms": result.execution_time_seconds * 1000,
                    "message": result.message,
                },

            )

    def summary(self) -> dict[str, int]:
        """
        Return rule summary.
        """

        total = len(self.registry)

        return {

            "total_rules": total,

            "enabled_rules": sum(

                rule.enabled

                for rule in self.registry.rules

            ),

            "disabled_rules": sum(

                not rule.enabled

                for rule in self.registry.rules

            ),

        }

    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Framework version.
        """

        return self.VERSION