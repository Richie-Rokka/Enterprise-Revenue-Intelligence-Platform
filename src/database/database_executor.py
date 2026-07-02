"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : database_executor.py
Package     : src.database
Purpose     : Enterprise Database Executor
Author      : ERIP
Version     : 2.1.0

Description
-----------
Provides a centralized service for executing SQL scripts against the
Enterprise Data Warehouse.

Responsibilities
----------------
- Execute SQL scripts
- Manage database transactions
- Measure execution time
- Log execution metrics
- Return standardized execution results

Future Enhancements
-------------------
- Retry policies
- Timeout management
- Audit logging
- Execution metrics
- Parallel execution
- Dependency resolution

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import text

from src.database.connection import get_engine
from src.observability import (
    Timer,
    get_logger,
)


logger = get_logger(__name__)


# =============================================================================
# Execution Result
# =============================================================================


@dataclass(slots=True)
class ExecutionResult:
    """
    Result of a database execution.
    """

    script_name: str

    success: bool

    execution_time_seconds: float

    error: str | None = None


# =============================================================================
# Database Executor
# =============================================================================


class DatabaseExecutor:
    """
    Enterprise Database Executor.

    Shared infrastructure service used by all platform
    frameworks for SQL execution.
    """

    def __init__(self) -> None:

        self.engine = get_engine()

    # -------------------------------------------------------------------------

    def execute(
        self,
        script_path: Path,
        script_name: str | None = None,
    ) -> ExecutionResult:
        """
        Execute a SQL script.

        Parameters
        ----------
        script_path
            Path to SQL script.

        script_name
            Optional display name.

        Returns
        -------
        ExecutionResult
        """

        if not script_path.exists():

            raise FileNotFoundError(script_path)

        if script_name is None:

            script_name = script_path.name

        logger.info(

            "Executing SQL Script: %s",

            script_name,

        )

        sql = script_path.read_text(

            encoding="utf-8"

        )

        if not sql.strip():
            raise ValueError(
                f"SQL script is empty: {script_name}"
            )

        try:

            with Timer() as timer:

                with self.engine.begin() as connection:

                    connection.execute(

                        text(sql)

                    )

            logger.info(

                "Completed: %s (%.2f sec)",

                script_name,

                timer.elapsed_seconds,

            )

            return ExecutionResult(

                script_name=script_name,

                success=True,

                execution_time_seconds=timer.elapsed_seconds,

            )

        except Exception as error:

            logger.exception(

                "Execution Failed: %s",

                script_name,

            )

            return ExecutionResult(

                script_name=script_name,

                success=False,

                execution_time_seconds=0.0,

                error=str(error),

            )

    # -------------------------------------------------------------------------

    def execute_many(
        self,
        scripts: list[Path],
    ) -> list[ExecutionResult]:
        """
        Execute multiple SQL scripts sequentially.
        """

        results: list[ExecutionResult] = []

        for script in scripts:

            result = self.execute(

                script_path=script,

                script_name=script.name,

            )

            results.append(result)

            if not result.success:

                raise RuntimeError(

                    f"Execution failed: {script.name}"

                )

        return results