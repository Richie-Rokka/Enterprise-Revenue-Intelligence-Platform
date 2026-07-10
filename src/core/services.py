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
Core Infrastructure

Warehouse Framework

Semantic Framework

Monitoring Framework

Quality Framework

ETL Framework

Extension Services

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

from src.monitoring.manager import MonitoringManager
from src.monitoring.validator import MonitoringValidator

from src.quality.manager import QualityManager
from src.quality.validator import QualityValidator

from src.warehouse.registry import DDLRegistry
from src.semantic.registry import SemanticRegistry
from src.monitoring.registry import MonitoringRegistry
from src.quality.registry import QualityRegistry

from src.runtime.lifecycle import RuntimeLifecycle
from src.runtime.manager import RuntimeManager

from src.database.health import DatabaseHealth

from src.quality.rules import RulesEngine
from src.quality.scorecard import ScorecardEngine
from src.quality.registry import (
    QualityRegistry,
    QualityRuleRegistry,
)


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

        self._database_health = None

        #
        # Runtime Framework
        #
        
        self._runtime_lifecycle = None
        
        self._runtime_manager = None

        #
        # Warehouse Framework
        #

        self._warehouse_registry = None

        self._warehouse_validator = None

        self._warehouse_manager = None

        #
        # Semantic Framework
        #

        self._semantic_registry = None

        self._semantic_validator = None

        self._semantic_manager = None

        #
        # Future Platform Services
        #

        #
        # Monitoring Framework
        #

        self._monitoring_registry = None

        self._monitoring_validator = None

        self._monitoring_manager = None

        #
        # Quality Framework
        #

        self._quality_registry = None

        self._quality_validator = None

        self._quality_manager = None

        self._rules_engine = None

        self._scorecard_engine = None


        self._etl_manager = None

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


    @property
    def database_health(self) -> DatabaseHealth:
        """
        Shared Database Health service.
        """

        if self._database_health is None:

            self._database_health = DatabaseHealth(

                engine=self.engine,

            )

        return self._database_health

    
    # =========================================================================
    # Runtime Framework
    # =========================================================================

    @property
    def runtime_lifecycle(self) -> RuntimeLifecycle:
        """
        Shared Runtime Lifecycle.
        """

        if self._runtime_lifecycle is None:

            self._runtime_lifecycle = RuntimeLifecycle()

        return self._runtime_lifecycle


    @property
    def runtime_manager(self) -> RuntimeManager:
        """
        Shared Runtime Manager.
        """

        if self._runtime_manager is None:

            self._runtime_manager = RuntimeManager(

                lifecycle=self.runtime_lifecycle,

            )

        return self._runtime_manager

    # =========================================================================
    # Warehouse
    # =========================================================================

    @property
    def warehouse_manager(self) -> WarehouseManager:
        """
        Shared Warehouse Manager.
        """

        if self._warehouse_manager is None:

            self._warehouse_manager = WarehouseManager(

            registry=self.warehouse_registry,

            validator=self.warehouse_validator,

            executor=self.database_executor,

            runtime=self.runtime_manager,

        )

        return self._warehouse_manager


    @property
    def warehouse_registry(self) -> DDLRegistry:
        """
        Shared Warehouse DDL Registry.
        """

        if self._warehouse_registry is None:

            self._warehouse_registry = DDLRegistry()

        return self._warehouse_registry

    @property
    def warehouse_validator(self) -> WarehouseValidator:
        """
        Shared Warehouse Validator.
        """

        if self._warehouse_validator is None:

            self._warehouse_validator = WarehouseValidator(

            engine=self.engine,

            )

        return self._warehouse_validator

    # =========================================================================
    # Semantic Framework
    # =========================================================================

    @property
    def semantic_registry(self) -> SemanticRegistry:
        """
        Shared Semantic Registry.
        """

        if self._semantic_registry is None:

            self._semantic_registry = SemanticRegistry()

        return self._semantic_registry

    # -------------------------------------------------------------------------

    @property
    def semantic_validator(self) -> SemanticValidator:
        """
        Shared Semantic Validator.
        """

        if self._semantic_validator is None:

            self._semantic_validator = SemanticValidator(

                engine=self.engine,

            )

        return self._semantic_validator

    # -------------------------------------------------------------------------

    @property
    def semantic_manager(self) -> SemanticManager:
        """
        Shared Semantic Manager.
        """

        if self._semantic_manager is None:

            self._semantic_manager = SemanticManager(

                registry=self.semantic_registry,

                validator=self.semantic_validator,

                executor=self.database_executor,

                runtime=self.runtime_manager,

            )

        return self._semantic_manager


    # =========================================================================
    # Monitoring Framework
    # =========================================================================

    @property
    def monitoring_registry(
        self,
    ) -> MonitoringRegistry:
        """
        Shared Monitoring Registry.
        """

        if self._monitoring_registry is None:

            self._monitoring_registry = MonitoringRegistry()

        return self._monitoring_registry


    # -------------------------------------------------------------------------


    @property
    def monitoring_validator(
    self,
    ) -> MonitoringValidator:
        """
        Shared Monitoring Validator.
        """

        if self._monitoring_validator is None:

            self._monitoring_validator = MonitoringValidator(

                registry=self.monitoring_registry,

                warehouse=self.warehouse_manager,

                semantic=self.semantic_manager,

                engine=self.engine,

            )

        return self._monitoring_validator


    # -------------------------------------------------------------------------


    @property
    def monitoring_manager(
        self,
    ) -> MonitoringManager:
        """
        Shared Monitoring Manager.
        """

        if self._monitoring_manager is None:

            self._monitoring_manager = MonitoringManager(

                registry=self.monitoring_registry,

                validator=self.monitoring_validator,

                executor=self.database_executor,

                warehouse=self.warehouse_manager,

                semantic=self.semantic_manager,

                runtime=self.runtime_manager,

            )

        return self._monitoring_manager


    # =========================================================================
    # Quality Framework
    # =========================================================================

    @property
    def quality_registry(self) -> QualityRegistry:
        """
        Shared Quality Registry.
        """

        if self._quality_registry is None:

            self._quality_registry = QualityRegistry()

        return self._quality_registry


    @property
    def quality_validator(self) -> QualityValidator:
        """
        Shared Quality Validator.
        """

        if self._quality_validator is None:

            self._quality_validator = QualityValidator(

                registry=self.quality_registry,

                engine=self.engine,

                warehouse=self.warehouse_manager,

                semantic=self.semantic_manager,

                monitoring=self.monitoring_manager,

            )

        return self._quality_validator


    @property
    def quality_manager(self) -> QualityManager:
        """
        Shared Quality Manager.
        """

        if self._quality_manager is None:

            self._quality_manager = QualityManager(

                registry=self.quality_registry,

                validator=self.quality_validator,

                warehouse=self.warehouse_manager,

                semantic=self.semantic_manager,

                monitoring=self.monitoring_manager,

                rules_engine=self.rules_engine,

            )

        return self._quality_manager

           
    @property
    def rules_engine(self) -> RulesEngine:
        
        if self._rules_engine is None:
        
            self._rules_engine = RulesEngine(

                executor=self.database_executor,

            )
        
        return self._rules_engine
        
    @property
    def scorecard_engine(self) -> ScorecardEngine:
        
        if self._scorecard_engine is None:
        
            self._scorecard_engine = ScorecardEngine(
        
                rules_engine=self.rules_engine,
        
            )
        
        return self._scorecard_engine
    
    # =========================================================================
    # Future Platform Services
    # =========================================================================

    @property
    def etl_manager(self):

        return self._etl_manager
    
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

    def register_cache(self, cache: Any) -> None:

        self._cache = cache

    def register_notifier(self, notifier: Any) -> None:
    
        self._notifier = notifier

    def register_scheduler(self, scheduler: Any) -> None:

        self._scheduler = scheduler

    def register_secrets(self, secrets: Any) -> None:

        self._secrets = secrets

      
    
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

            "database_health": self._database_health is not None,

            #
            # Runtime
            #

            "runtime_lifecycle": self._runtime_lifecycle is not None,

            "runtime_manager": self._runtime_manager is not None,

            #
            # Warehouse
            #

            "warehouse_registry": self._warehouse_registry is not None,

            "warehouse_manager": self._warehouse_manager is not None,

            "warehouse_validator": self._warehouse_validator is not None,

            #
            # Semantic
            #

            "semantic_registry": self._semantic_registry is not None,

            "semantic_manager": self._semantic_manager is not None,

            "semantic_validator": self._semantic_validator is not None,

            #
            # Monitoring
            #

            "monitoring_registry": self._monitoring_registry is not None,

            "monitoring_validator": self._monitoring_validator is not None,

            "monitoring_manager": self._monitoring_manager is not None,

            #
            # Quality
            #

            "quality_registry": self._quality_registry is not None,

            "quality_validator": self._quality_validator is not None,

            "quality_manager": self._quality_manager is not None,

            "rules_engine":
                self._rules_engine is not None,

            "scorecard_engine":
                self._scorecard_engine is not None,

            #
            # Extension Services
            #

            "etl_manager": self._etl_manager is not None,
                     
            
        }