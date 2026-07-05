"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : models.py
Package     : src.quality
Purpose     : Enterprise Data Quality Models
Author      : ERIP
Version     : 2.0.0

Description
-----------
Shared data models used throughout the Enterprise Data Quality Framework.

Responsibilities
----------------
- Quality validation models
- Business rule models
- Quality scorecards
- Quality summaries
- Framework status models

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


# =============================================================================
# Quality Rule
# =============================================================================


@dataclass(slots=True)
class QualityRule:
    """
    Enterprise data quality rule.
    """

    name: str

    description: str

    category: str

    severity: str

    enabled: bool = True


# =============================================================================
# Quality Check Result
# =============================================================================


@dataclass(slots=True)
class QualityCheckResult:
    """
    Result of a single quality rule.
    """

    rule_name: str

    passed: bool

    rows_checked: int

    rows_failed: int

    execution_time_seconds: float

    message: str | None = None


# =============================================================================
# Data Quality Validation
# =============================================================================


@dataclass(slots=True)
class DataQualityValidationResult:
    """
    Overall framework validation.
    """

    passed: bool

    checks_performed: int

    failures: list[str]


# =============================================================================
# Quality Scorecard
# =============================================================================


@dataclass(slots=True)
class QualityScorecard:
    """
    Enterprise data quality scorecard.
    """

    completeness_score: float

    uniqueness_score: float

    consistency_score: float

    referential_integrity_score: float

    freshness_score: float

    overall_score: float

    grade: str

    generated_at: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# Quality Summary
# =============================================================================


@dataclass(slots=True)
class QualitySummary:
    """
    Enterprise quality summary.
    """

    total_rules: int

    rules_passed: int

    rules_failed: int

    total_rows_checked: int

    total_rows_failed: int

    execution_time_seconds: float


# =============================================================================
# Business Rule Summary
# =============================================================================


@dataclass(slots=True)
class BusinessRuleSummary:
    """
    Summary of business rule execution.
    """

    rules_executed: int

    rules_passed: int

    rules_failed: int

    critical_failures: int

    warning_failures: int


# =============================================================================
# Data Freshness
# =============================================================================


@dataclass(slots=True)
class DataFreshness:
    """
    Data freshness metrics.
    """

    table_name: str

    last_refresh: datetime

    expected_refresh_interval_hours: int

    hours_since_refresh: float

    is_current: bool


# =============================================================================
# Referential Integrity
# =============================================================================


@dataclass(slots=True)
class ReferentialIntegrityResult:
    """
    Referential integrity assessment.
    """

    relationship: str

    parent_table: str

    child_table: str

    orphan_records: int

    passed: bool


# =============================================================================
# Completeness
# =============================================================================


@dataclass(slots=True)
class CompletenessResult:
    """
    Completeness assessment.
    """

    table_name: str

    column_name: str

    total_rows: int

    populated_rows: int

    completeness_percent: float

    passed: bool


# =============================================================================
# Uniqueness
# =============================================================================


@dataclass(slots=True)
class UniquenessResult:
    """
    Uniqueness assessment.
    """

    table_name: str

    column_name: str

    duplicate_rows: int

    uniqueness_percent: float

    passed: bool


# =============================================================================
# Quality Dashboard
# =============================================================================


@dataclass(slots=True)
class QualityDashboard:
    """
    Enterprise Data Quality dashboard.
    """

    validation: DataQualityValidationResult

    summary: QualitySummary

    scorecard: QualityScorecard

    business_rules: BusinessRuleSummary