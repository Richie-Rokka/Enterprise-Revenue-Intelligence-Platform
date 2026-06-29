"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    base.py

Purpose:
    Base class for the Enterprise Validation Framework.

Description:
    Provides common functionality shared by all ERIP validators.

Responsibilities
----------------
• Database connection management
• Safe SQL execution
• Schema validation
• Table validation
• Constraint validation
• Index validation
• Standardized success/failure responses

Author:
    Abodunrin Oketade

Platform:
    Enterprise Revenue Intelligence Platform (ERIP)

Version:
    2.1.0
===============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import closing
from typing import Any

from sqlalchemy import text

from src.database.connection import get_connection

from .models import ValidationResult


# ==============================================================================
# BASE VALIDATOR
# ==============================================================================

class BaseValidator(ABC):
    """
    Base class for all ERIP validators.

    Every validator inherits the database utilities provided here.
    """

    NAME = "Base Validator"

    # -------------------------------------------------------------------------

    @abstractmethod
    def validate(self) -> ValidationResult:
        """
        Execute validation.

        Returns
        -------
        ValidationResult
        """

        raise NotImplementedError

    # -------------------------------------------------------------------------
    # SQL EXECUTION
    # -------------------------------------------------------------------------

    def execute_scalar(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> Any:
        """
        Execute a SQL statement that returns a single value.
        """

        with closing(get_connection()) as connection:

            result = connection.execute(
                text(query),
                parameters or {},
            )

            return result.scalar()

    # -------------------------------------------------------------------------

    def execute_all(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ):
        """
        Execute a SQL statement returning multiple rows.
        """

        with closing(get_connection()) as connection:

            result = connection.execute(
                text(query),
                parameters or {},
            )

            return result.fetchall()

    # -------------------------------------------------------------------------
    # SCHEMA HELPERS
    # -------------------------------------------------------------------------

    def schema_exists(
        self,
        schema_name: str,
    ) -> bool:

        query = """
            SELECT EXISTS
            (
                SELECT 1
                FROM information_schema.schemata
                WHERE schema_name = :schema_name
            )
        """

        return bool(

            self.execute_scalar(

                query,

                {"schema_name": schema_name}

            )

        )

    # -------------------------------------------------------------------------
    # TABLE HELPERS
    # -------------------------------------------------------------------------

    def table_exists(
        self,
        schema_name: str,
        table_name: str,
    ) -> bool:

        query = """
            SELECT EXISTS
            (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = :schema_name
                  AND table_name = :table_name
            )
        """

        return bool(

            self.execute_scalar(

                query,

                {

                    "schema_name": schema_name,

                    "table_name": table_name,

                }

            )

        )

    # -------------------------------------------------------------------------
    # INDEX HELPERS
    # -------------------------------------------------------------------------

    def index_exists(
        self,
        index_name: str,
    ) -> bool:

        query = """
            SELECT EXISTS
            (
                SELECT 1
                FROM pg_indexes
                WHERE indexname = :index_name
            )
        """

        return bool(

            self.execute_scalar(

                query,

                {

                    "index_name": index_name

                }

            )

        )

    # -------------------------------------------------------------------------
    # CONSTRAINT HELPERS
    # -------------------------------------------------------------------------

    def constraint_exists(
        self,
        schema_name: str,
        table_name: str,
        constraint_name: str,
    ) -> bool:

        query = """
            SELECT EXISTS
            (
                SELECT 1
                FROM information_schema.table_constraints
                WHERE table_schema = :schema_name
                  AND table_name = :table_name
                  AND constraint_name = :constraint_name
            )
        """

        return bool(

            self.execute_scalar(

                query,

                {

                    "schema_name": schema_name,

                    "table_name": table_name,

                    "constraint_name": constraint_name,

                }

            )

        )

    # -------------------------------------------------------------------------
    # RESULT HELPERS
    # -------------------------------------------------------------------------

    def success(
        self,
        name: str,
        message: str,
    ) -> ValidationResult:

        return ValidationResult(

            name=name,

            passed=True,

            message=message,

        )

    # -------------------------------------------------------------------------

    def failure(
        self,
        name: str,
        message: str,
    ) -> ValidationResult:

        return ValidationResult(

            name=name,

            passed=False,

            message=message,

        )