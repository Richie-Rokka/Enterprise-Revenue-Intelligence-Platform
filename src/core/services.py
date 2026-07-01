"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : services.py
Package     : src.core
Purpose     : Enterprise Service Container
Author      : ERIP
Version     : 2.1.0

Description
-----------
Central dependency injection container for the Enterprise Revenue
Intelligence Platform.

Responsibilities
----------------
- Central Configuration
- Database Engine
- Logger
- Future Enterprise Services

Design
------
• Singleton services
• Lazy initialization
• Dependency Injection
• Single Source of Configuration

===============================================================================
"""

from __future__ import annotations

from typing import Any

from src.config.config import config

from src.database.connection import get_engine

from src.observability import get_logger


class ServiceContainer:
    """
    Enterprise dependency injection container.

    This class owns all shared platform services and ensures
    only one instance of each service exists during execution.
    """

    def __init__(self) -> None:

        # ---------------------------------------------------------------------
        # Core Services
        # ---------------------------------------------------------------------

        self._engine = None
        self._logger = None

        # ---------------------------------------------------------------------
        # Future Enterprise Services
        # ---------------------------------------------------------------------

        self._metrics = None
        self._notifier = None
        self._cache = None
        self._scheduler = None
        self._secrets = None

    # =====================================================================
    # Configuration
    # =====================================================================

    @property
    def config(self):
        """
        Return the central platform configuration.
        """

        return config

    # =====================================================================
    # Database
    # =====================================================================

    @property
    def engine(self):
        """
        Return singleton SQLAlchemy engine.
        """

        if self._engine is None:

            self._engine = get_engine()

        return self._engine

    # =====================================================================
    # Logger
    # =====================================================================

    @property
    def logger(self):
        """
        Return platform logger.
        """

        if self._logger is None:

            self._logger = get_logger("ERIP")

        return self._logger

    # =====================================================================
    # Future Enterprise Services
    # =====================================================================

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

    # =====================================================================
    # Registration
    # =====================================================================

    def register_metrics(
        self,
        metrics: Any,
    ) -> None:

        self._metrics = metrics

    def register_notifier(
        self,
        notifier: Any,
    ) -> None:

        self._notifier = notifier

    def register_cache(
        self,
        cache: Any,
    ) -> None:

        self._cache = cache

    def register_scheduler(
        self,
        scheduler: Any,
    ) -> None:

        self._scheduler = scheduler

    def register_secrets(
        self,
        secrets: Any,
    ) -> None:

        self._secrets = secrets

    # =====================================================================
    # Diagnostics
    # =====================================================================

    def summary(self) -> dict[str, bool]:
        """
        Return service initialization status.
        """

        return {

            "config": True,

            "engine": self._engine is not None,

            "logger": self._logger is not None,

            "metrics": self._metrics is not None,

            "notifier": self._notifier is not None,

            "cache": self._cache is not None,

            "scheduler": self._scheduler is not None,

            "secrets": self._secrets is not None,
        }