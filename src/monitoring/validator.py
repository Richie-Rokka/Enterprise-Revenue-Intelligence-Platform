"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : validator.py
Package     : src.monitoring
Purpose     : Enterprise Monitoring Validator
Author      : ERIP
Version     : 2.0.0

Description
-----------
Validates the Monitoring Framework and its dependencies before
monitoring services are executed.

Responsibilities
----------------
- Validate monitoring registry
- Validate monitoring SQL assets
- Validate database connectivity
- Validate warehouse framework
- Validate semantic framework

===============================================================================
"""

from __future__ import annotations

from sqlalchemy import text

from src.database.connection import get_engine
from src.observability import get_logger

from src.semantic.manager import SemanticManager
from src.warehouse.manager import WarehouseManager

from .models import MonitoringValidationResult
from .registry import MonitoringRegistry


logger = get_logger(__name__)


# =============================================================================
# Monitoring Validator
# =============================================================================


class MonitoringValidator:
    """
    Enterprise Monitoring Validator.
    """

    VERSION = "2.0.0"

    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self.registry = MonitoringRegistry()

        self.engine = get_engine()

        self.warehouse = WarehouseManager()

        self.semantic = SemanticManager()

    # -------------------------------------------------------------------------

    def validate(self) -> MonitoringValidationResult:
        """
        Validate the Monitoring Framework.

        Returns
        -------
        MonitoringValidationResult
        """

        logger.info("=" * 60)
        logger.info("Starting Monitoring Framework Validation")
        logger.info("=" * 60)

        failures: list[str] = []

        checks = 0

        # -----------------------------------------------------------------
        # Registry
        # -----------------------------------------------------------------

        try:

            self.registry.validate()

            checks += 1

        except Exception as error:

            failures.append(

                f"Monitoring Registry: {error}"

            )

        # -----------------------------------------------------------------
        # Database Connectivity
        # -----------------------------------------------------------------

        try:

            with self.engine.begin() as connection:

                connection.execute(

                    text("SELECT 1")

                )

            checks += 1

        except Exception as error:

            failures.append(

                f"Database Connection: {error}"

            )

        # -----------------------------------------------------------------
        # Warehouse
        # -----------------------------------------------------------------

        try:

            if self.warehouse.status() != "READY":

                failures.append(

                    "Warehouse Framework is not READY."

                )

            else:

                checks += 1

        except Exception as error:

            failures.append(

                f"Warehouse Validation: {error}"

            )

        # -----------------------------------------------------------------
        # Semantic
        # -----------------------------------------------------------------

        try:

            if self.semantic.status() != "READY":

                failures.append(

                    "Semantic Framework is not READY."

                )

            else:

                checks += 1

        except Exception as error:

            failures.append(

                f"Semantic Validation: {error}"

            )

        # -----------------------------------------------------------------
        # Monitoring Assets
        # -----------------------------------------------------------------

        try:

            if len(self.registry) == 0:

                failures.append(

                    "No monitoring assets were discovered."

                )

            else:

                checks += 1

        except Exception as error:

            failures.append(

                f"Monitoring Assets: {error}"

            )

        # -----------------------------------------------------------------
        # Result
        # -----------------------------------------------------------------

        passed = len(failures) == 0

        if passed:

            logger.info(

                "Monitoring validation successful."

            )

        else:

            logger.error(

                "Monitoring validation failed."

            )

            for failure in failures:

                logger.error(failure)

        return MonitoringValidationResult(

            passed=passed,

            checks_performed=checks,

            failures=failures,

        )

    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Framework version.
        """

        return self.VERSION