"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : manager.py
Package     : src.quality
Purpose     : Enterprise Data Quality Manager
Author      : ERIP
Version     : 2.0.0

Description
-----------
Public interface for all Enterprise Data Quality operations.

Responsibilities
----------------
- Execute framework validation
- Generate quality summary
- Generate quality scorecard
- Report framework status
- Serve as the public façade for the Data Quality Framework

===============================================================================
"""

from __future__ import annotations

from src.monitoring.manager import MonitoringManager
from src.observability import get_logger
from src.semantic.manager import SemanticManager
from src.warehouse.manager import WarehouseManager
from .registry import QualityRegistry

from .models import (
    BusinessRuleSummary,
    DataQualityValidationResult,
    QualityDashboard,
    QualityScorecard,
    QualitySummary,
)
from .validator import QualityValidator
from .rules import RulesEngine


logger = get_logger(__name__)


# =============================================================================
# Quality Manager
# =============================================================================


class QualityManager:
    """
    Enterprise Data Quality Manager.

    Public façade for all data quality operations.
    """

    VERSION = "2.0.0"

    # -------------------------------------------------------------------------

    def __init__(
        self,
        *,
        registry: QualityRegistry,
        validator: QualityValidator,
        warehouse: WarehouseManager,
        semantic: SemanticManager,
        monitoring: MonitoringManager,
        rules_engine: RulesEngine,
    ) -> None:
        """
        Construct the Enterprise Data Quality Manager.

        Parameters
        ----------
        registry
            Shared Quality Registry.

        validator
            Shared Data Quality Validator.

        warehouse
            Shared Warehouse Manager.

        semantic
            Shared Semantic Manager.

        monitoring
            Shared Monitoring Manager.
        """

        self.registry = registry

        self.validator = validator

        self.warehouse = warehouse

        self.semantic = semantic

        self.monitoring = monitoring

        self.rules_engine = rules_engine

        self._rule_results = None

        self._rules_dirty = True

        # ---------------------------------------------------------------------
        # Runtime State
        # ---------------------------------------------------------------------

        self._validation_result: DataQualityValidationResult | None = None

        self._validation_dirty: bool = True

        # ---------------------------------------------------------------------
        # Rule Execution Cache
        # ---------------------------------------------------------------------

        self._rule_results = None

        self._rules_dirty = True

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def validate(self) -> DataQualityValidationResult:
        """
        Validate the Data Quality Framework.
        """

        if self._validation_dirty:

            self._validation_result = self.validator.validate()

            self._validation_dirty = False

        return self._validation_result

    def execute_rules(self):
        """
        Execute quality rules once per framework execution.
        """

        if self._rules_dirty:

            self._rule_results = self.rules_engine.execute()

            self._rules_dirty = False

        return self._rule_results

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    def summary(self) -> QualitySummary:
        """
        Return a quality execution summary.

        NOTE
        ----
        Placeholder implementation until rules.py is introduced.
        """

        results = self.execute_rules()

        return QualitySummary(

            total_rules=len(results),

            rules_passed=sum(r.passed for r in results),

            rules_failed=sum(not r.passed for r in results),

            total_rows_checked=sum(r.rows_checked for r in results),

            total_rows_failed=sum(r.rows_failed for r in results),

            execution_time_seconds=sum(
                r.execution_time_seconds
                for r in results
            ),

)
    # -------------------------------------------------------------------------
    # Scorecard
    # -------------------------------------------------------------------------

    def scorecard(self) -> QualityScorecard:
        """
        Return enterprise quality scorecard.

        NOTE
        ----
        Placeholder implementation until scorecard.py is introduced.
        """

        return QualityScorecard(

            completeness_score=100.0,

            uniqueness_score=100.0,

            consistency_score=100.0,

            referential_integrity_score=100.0,

            freshness_score=100.0,

            overall_score=100.0,

            grade="A+",

        )

    # -------------------------------------------------------------------------
    # Business Rules
    # -------------------------------------------------------------------------

    def rules(self) -> BusinessRuleSummary:
        """
        Return business rule execution summary.

        NOTE
        ----
        Placeholder implementation until rules.py is introduced.
        """

        results = self.execute_rules()

        return BusinessRuleSummary(

            rules_executed=len(results),

            rules_passed=sum(r.passed for r in results),

            rules_failed=sum(not r.passed for r in results),

            critical_failures=0,

            warning_failures=0,

        )

    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    def dashboard(self) -> QualityDashboard:
        """
        Return enterprise quality dashboard.
        """

        self.execute_rules()

        summary = self.summary()

        scorecard = self.scorecard()

        rules = self.rules()
        
        return QualityDashboard(

            validation=self.validate(),

            summary=summary,

            scorecard=scorecard,

            business_rules=rules,

        )

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    def status(self) -> str:
        """
        Return framework status.
        """

        validation = self.validate()

        return "READY" if validation.passed else "INVALID"

    # -------------------------------------------------------------------------
    # Version
    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Return framework version.
        """

        return self.VERSION