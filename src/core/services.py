"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : services.py
Package     : src.core
Purpose     : Enterprise Service Container
Author      : ERIP
Version     : 2.2.0

Description
-----------
Central dependency injection container for the Enterprise Revenue
Intelligence Platform.

Responsibilities
----------------
- Central Configuration
- Database Engine
- Database Executor
- Logger
- Warehouse Framework
- Semantic Framework
- Future Enterprise Services

Design
------
• Singleton Services
• Lazy Initialization
• Dependency Injection
• Single Source of Configuration

===============================================================================
"""

from __future__ import annotations

from typing import Any

from src.config.config import config

from src.database.connection import get_engine
from src.database.database_executor import DatabaseExecutor

from src.observability import get_logger

from src.warehouse.manager import WarehouseManager
from src.warehouse.validator import WarehouseValidator

from src.semantic.manager import SemanticManager
from src.semantic.validator import SemanticValidator


# =============================================================================
# Service Container
# =============================================================================


class ServiceContainer:
    """
    Enterprise dependency injection container.

    Owns all shared services used throughout ERIP and ensures
    only one instance of each service exists during platform
    execution.
    """

    # -------------------------------------------------------------------------
    # Construction
    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        #
        # Core Infrastructure
        #

        self._engine = None

        self._logger = None

        self._database_executor = None

        #
        # Warehouse Framework
        #

        self._warehouse_manager = None

        self._warehouse_validator = None

        #
        # Semantic Framework
        #

        self._semantic_manager = None

        self._semantic_validator = None

        #
        # Future Platform Services
        #

        self._etl_manager = None

        self._quality_manager = None

        self._monitoring_manager = None

        self._metrics = None

        self._notifier = None

        self._cache = None

        self._scheduler = None

        self._secrets = None

    # =========================================================================
    # Configuration
    # =========================================================================

    @property
    def config(self):
        """
        Return central platform configuration.
        """

        return config

    # =========================================================================
    # Logger
    # =========================================================================

    @property
    def logger(self):
        """
        Return singleton platform logger.
        """

        if self._logger is None:

            self._logger = get_logger("ERIP")

        return self._logger

    # =========================================================================
    # Database
    # =========================================================================

    @property
    def engine(self):
        """
        Return singleton SQLAlchemy engine.
        """

        if self._engine is None:

            self._engine = get_engine()

        return self._engine

    # =========================================================================
    # Database Executor
    # =========================================================================

    @property
    def database_executor(self) -> DatabaseExecutor:
        """
        Shared SQL execution service.
        """

        if self._database_executor is None:

            self._database_executor = DatabaseExecutor()

        return self._database_executor

    # =========================================================================
    # Warehouse
    # =========================================================================

    @property
    def warehouse_manager(self) -> WarehouseManager:
        """
        Warehouse Manager.
        """

        if self._warehouse_manager is None:

            self._warehouse_manager = WarehouseManager()

        return self._warehouse_manager

    @property
    def warehouse_validator(self) -> WarehouseValidator:
        """
        Warehouse Validator.
        """

        if self._warehouse_validator is None:

            self._warehouse_validator = WarehouseValidator()

        return self._warehouse_validator

    # =========================================================================
    # Semantic
    # =========================================================================

    @property
    def semantic_manager(self) -> SemanticManager:
        """
        Semantic Manager.
        """

        if self._semantic_manager is None:

            self._semantic_manager = SemanticManager()

        return self._semantic_manager

    @property
    def semantic_validator(self) -> SemanticValidator:
        """
        Semantic Validator.
        """

        if self._semantic_validator is None:

            self._semantic_validator = SemanticValidator()

        return self._semantic_validator

    # =========================================================================
    # Future Platform Services
    # =========================================================================

    @property
    def etl_manager(self):

        return self._etl_manager

    @property
    def quality_manager(self):

        return self._quality_manager

    @property
    def monitoring_manager(self):

        return self._monitoring_manager

    @property
    def metrics(self):

        return self._metrics

    @property
    def notifier(self):

        return self._notifier

    @property
    def cache(self):

        return self._cache

    @property
    def scheduler(self):

        return self._scheduler

    @property
    def secrets(self):

        return self._secrets

    # =========================================================================
    # Registration
    # =========================================================================

    def register_metrics(self, metrics: Any) -> None:

        self._metrics = metrics

    def register_notifier(self, notifier: Any) -> None:

        self._notifier = notifier

    def register_cache(self, cache: Any) -> None:

        self._cache = cache

    def register_scheduler(self, scheduler: Any) -> None:

        self._scheduler = scheduler

    def register_secrets(self, secrets: Any) -> None:

        self._secrets = secrets

    def register_etl_manager(self, manager: Any) -> None:

        self._etl_manager = manager

    def register_quality_manager(self, manager: Any) -> None:

        self._quality_manager = manager

    def register_monitoring_manager(self, manager: Any) -> None:

        self._monitoring_manager = manager

    # =========================================================================
    # Diagnostics
    # =========================================================================

    def summary(self) -> dict[str, bool]:
        """
        Return initialization status of all platform services.
        """

        return {

            #
            # Core
            #

            "config": True,

            "engine": self._engine is not None,

            "logger": self._logger is not None,

            "database_executor": self._database_executor is not None,

            #
            # Warehouse
            #

            "warehouse_manager": self._warehouse_manager is not None,

            "warehouse_validator": self._warehouse_validator is not None,

            #
            # Semantic
            #

            "semantic_manager": self._semantic_manager is not None,

            "semantic_validator": self._semantic_validator is not None,

            #
            # Future
            #

            "etl_manager": self._etl_manager is not None,

            "quality_manager": self._quality_manager is not None,

            "monitoring_manager": self._monitoring_manager is not None,

            "metrics": self._metrics is not None,

            "notifier": self._notifier is not None,

            "cache": self._cache is not None,

            "scheduler": self._scheduler is not None,

            "secrets": self._secrets is not None,

        }