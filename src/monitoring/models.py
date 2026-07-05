"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : models.py
Package     : src.monitoring
Purpose     : Monitoring Framework Models
Author      : ERIP
Version     : 2.0.0

Description
-----------
Shared data models used throughout the Enterprise Monitoring Framework.

Responsibilities
----------------
- Platform health models
- Runtime metrics
- Deployment metrics
- Monitoring summaries
- Dashboard models

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


# =============================================================================
# Platform Health
# =============================================================================


@dataclass(slots=True)
class PlatformHealth:
    """
    Overall platform health.
    """

    database: str

    warehouse: str

    semantic: str

    overall: str

    checked_at: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# Runtime Statistics
# =============================================================================


@dataclass(slots=True)
class RuntimeStatistics:
    """
    Runtime performance metrics.
    """

    execution_time_seconds: float

    memory_usage_mb: float

    cpu_usage_percent: float | None = None

    collected_at: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# Deployment Statistics
# =============================================================================


@dataclass(slots=True)
class DeploymentStatistics:
    """
    Deployment metrics.
    """

    deployment_success: bool

    scripts_executed: int

    execution_time_seconds: float

    deployed_at: datetime = field(default_factory=datetime.utcnow)


# =============================================================================
# Warehouse Statistics
# =============================================================================


@dataclass(slots=True)
class WarehouseStatistics:
    """
    Warehouse operational statistics.
    """

    dimensions_loaded: int

    fact_tables_loaded: int

    rows_processed: int

    execution_time_seconds: float


# =============================================================================
# Semantic Statistics
# =============================================================================


@dataclass(slots=True)
class SemanticStatistics:
    """
    Semantic layer statistics.
    """

    views_deployed: int

    validation_checks: int

    deployment_success: bool

    execution_time_seconds: float


# =============================================================================
# Monitoring Dashboard
# =============================================================================


@dataclass(slots=True)
class MonitoringDashboard:
    """
    Enterprise monitoring dashboard.
    """

    platform_health: PlatformHealth

    runtime: RuntimeStatistics

    deployment: DeploymentStatistics

    warehouse: WarehouseStatistics

    semantic: SemanticStatistics


# =============================================================================
# Monitoring Validation
# =============================================================================


@dataclass(slots=True)
class MonitoringValidationResult:
    """
    Monitoring framework validation.
    """

    passed: bool

    checks_performed: int

    failures: list[str]