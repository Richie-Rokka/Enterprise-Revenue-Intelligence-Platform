"""
Enterprise Revenue Intelligence Platform (ERIP)

Warehouse SQL Executor

Executes warehouse SQL deployment scripts with
transaction management, logging, and execution metrics.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import text

from src.database import get_engine
from src.observability import (
    Timer,
    get_logger,
)

from .registry import SQLScript


logger = get_logger(__name__)


@dataclass(slots=True)
class ExecutionResult:
    """
    Result of a SQL script execution.
    """

    filename: str

    success: bool

    execution_time_seconds: float

    error: str | None = None


class SQLExecutor:
    """
    Enterprise SQL Executor.

    Executes SQL scripts using transactional execution.
    """

    def __init__(self):

        self.engine = get_engine()

    def execute(
        self,
        script: SQLScript,
    ) -> ExecutionResult:
        """
        Execute a single SQL script.

        Parameters
        ----------
        script : SQLScript

        Returns
        -------
        ExecutionResult
        """

        logger.info(
            "Executing SQL Script: %s",
            script.filename,
        )

        if not script.path.exists():

            raise FileNotFoundError(
                script.path
            )

        sql = script.path.read_text(
            encoding="utf-8"
        )

        try:

            with Timer() as timer:

                with self.engine.begin() as connection:

                    connection.execute(
                        text(sql)
                    )

            logger.info(
                "Completed: %s (%.2f sec)",
                script.filename,
                timer.elapsed_seconds,
            )

            return ExecutionResult(

                filename=script.filename,

                success=True,

                execution_time_seconds=timer.elapsed_seconds,
            )

        except Exception as error:

            logger.exception(
                "Failed: %s",
                script.filename,
            )

            return ExecutionResult(

                filename=script.filename,

                success=False,

                execution_time_seconds=0.0,

                error=str(error),
            )

    def execute_all(
        self,
        scripts: list[SQLScript],
    ) -> list[ExecutionResult]:
        """
        Execute multiple SQL scripts.
        """

        results = []

        for script in scripts:

            result = self.execute(
                script
            )

            results.append(
                result
            )

            if not result.success:

                raise RuntimeError(

                    f"Warehouse deployment failed at "

                    f"{script.filename}"

                )

        return results