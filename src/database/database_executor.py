"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : database_executor.py
Package     : src.database
Purpose     : Enterprise Database Executor
Author      : ERIP
Version     : 2.2.0

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

Capabilities
------------
- Execute SQL files
- Execute SQL statements
- Transaction management
- Execution timing
- Enterprise logging
- Standardized execution results

Future Enhancements
-------------------
- Retry policies
- Timeout management
- Audit logging
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

    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------

    script_name: str

    success: bool

    execution_time_seconds: float

    # -------------------------------------------------------------------------
    # Telemetry
    # -------------------------------------------------------------------------

    rows_processed: int = 0

    query_result: dict | None = None

    # -------------------------------------------------------------------------
    # Error
    # -------------------------------------------------------------------------

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

                    result = connection.execute(
                        text(sql)
                    )

                    query_result = None

                    if result.returns_rows:

                        row = result.mappings().first()

                        if row:

                            query_result = dict(row)

                rows_processed = result.rowcount

                if rows_processed is None:

                    rows_processed = 0

                elif rows_processed < 0:

                    rows_processed = 0


            logger.info(

                "Completed: %s (%.2f sec)",

                script_name,

                timer.elapsed_seconds,

            )

            return ExecutionResult(

                script_name=script_name,

                success=True,

                execution_time_seconds=timer.elapsed_seconds,

                rows_processed=rows_processed,

                query_result=query_result,

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

    def execute_sql(
        self,
        sql: str,
        operation_name: str = "SQL Operation",
    ) -> ExecutionResult:
        """
        Execute an arbitrary SQL statement.

        Parameters
        ----------
        sql
            SQL statement(s) to execute.

        operation_name
            Friendly name for logging.

        Returns
        -------
        ExecutionResult
        """

        if not sql.strip():

            raise ValueError(

                "SQL statement is empty."

            )

        logger.info(

            "Executing SQL Operation: %s",

            operation_name,

        )

        try:

            

            with Timer() as timer:

                with self.engine.begin() as connection:

                    result = connection.execute(

                        text(sql)

                    )

                    rows_processed = result.rowcount

                    if rows_processed is None:

                        rows_processed = 0

                    elif rows_processed < 0:

                        rows_processed = 0

            logger.info(

                "Completed: %s (%.2f sec)",

                operation_name,

                timer.elapsed_seconds,

            )

            return ExecutionResult(

                script_name=operation_name,

                success=True,

                execution_time_seconds=timer.elapsed_seconds,

                rows_processed=rows_processed,

            )

        except Exception as error:

            logger.exception(

                "Execution Failed: %s",

                operation_name,

            )

            return ExecutionResult(

                script_name=operation_name,

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