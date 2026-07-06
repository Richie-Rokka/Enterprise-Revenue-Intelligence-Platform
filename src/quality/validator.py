"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : validator.py
Package     : src.quality
Purpose     : Enterprise Data Quality Validator
Author      : ERIP
Version     : 2.0.0

Description
-----------
Validates the Enterprise Data Quality Framework before quality
services are executed.

Responsibilities
----------------
- Validate Quality Registry
- Validate database connectivity
- Validate Warehouse Framework
- Validate Semantic Framework
- Validate Monitoring Framework
- Validate quality assets

===============================================================================
"""

from __future__ import annotations

from sqlalchemy import text

from sqlalchemy.engine import Engine
from src.monitoring.manager import MonitoringManager
from src.observability import get_logger
from src.semantic.manager import SemanticManager
from src.warehouse.manager import WarehouseManager

from .models import DataQualityValidationResult
from .registry import QualityRegistry


logger = get_logger(__name__)


# =============================================================================
# Quality Validator
# =============================================================================


class QualityValidator:
    """
    Enterprise Data Quality Validator.
    """

    VERSION = "2.0.0"

    # -------------------------------------------------------------------------

    def __init__(
        self,
        *,
        registry: QualityRegistry,
        engine: Engine,
        warehouse: WarehouseManager,
        semantic: SemanticManager,
        monitoring: MonitoringManager,
    ) -> None:
        """
        Construct the Enterprise Data Quality Validator.

        Parameters
        ----------
        registry
            Shared Quality Registry.

        engine
            Shared SQLAlchemy engine.

        warehouse
            Shared Warehouse Manager.

        semantic
            Shared Semantic Manager.

        monitoring
            Shared Monitoring Manager.
        """

        self.registry = registry

        self.engine = engine

        self.warehouse = warehouse

        self.semantic = semantic

        self.monitoring = monitoring

    # -------------------------------------------------------------------------

    def validate(self) -> DataQualityValidationResult:
        """
        Validate the Data Quality Framework.

        Returns
        -------
        DataQualityValidationResult
        """

        logger.info("=" * 60)
        logger.info("Starting Data Quality Framework Validation")
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

                f"Quality Registry: {error}"

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
        # Warehouse Framework
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
        # Semantic Framework
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
        # Monitoring Framework
        # -----------------------------------------------------------------

        try:

            if self.monitoring.status() != "READY":

                failures.append(

                    "Monitoring Framework is not READY."

                )

            else:

                checks += 1

        except Exception as error:

            failures.append(

                f"Monitoring Validation: {error}"

            )

        # -----------------------------------------------------------------
        # Quality Assets
        # -----------------------------------------------------------------

        try:

            if len(self.registry) == 0:

                failures.append(

                    "No quality assets were discovered."

                )

            else:

                checks += 1

        except Exception as error:

            failures.append(

                f"Quality Assets: {error}"

            )

        # -----------------------------------------------------------------
        # Validation Result
        # -----------------------------------------------------------------

        passed = len(failures) == 0

        if passed:

            logger.info(

                "Data Quality validation successful."

            )

        else:

            logger.error(

                "Data Quality validation failed."

            )

            for failure in failures:

                logger.error(failure)

        return DataQualityValidationResult(

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