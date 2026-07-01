"""
audit.py
Enterprise Revenue Intelligence Platform

Purpose
-------
Provides a centralized audit framework for monitoring
ETL pipeline executions, table loads, and data quality.

Author
------
Enterprise Revenue Intelligence Platform
"""

from datetime import datetime

from sqlalchemy import text

from src.utils.logger import get_logger


logger = get_logger(__name__)


class AuditManager:
    """
    Centralized audit manager for ETL monitoring.
    """

    def __init__(self, engine):

        self.engine = engine

        self.run_id = None

        self.start_time = None


    # ======================================================
    # START PIPELINE
    # ======================================================

    def start_run(
        self,
        pipeline_name
    ):
        """
        Create a new ETL run record.

        Returns
        -------
        int
            Newly created run_id.
        """

        self.start_time = datetime.now()

        with self.engine.begin() as connection:

            result = connection.execute(

                text(
                    """
                    INSERT INTO analytics.etl_run_history
                    (
                        pipeline_name,
                        start_time,
                        status
                    )

                    VALUES
                    (
                        :pipeline_name,
                        :start_time,
                        'Running'
                    )

                    RETURNING run_id;
                    """
                ),

                {
                    "pipeline_name": pipeline_name,
                    "start_time": self.start_time
                }

            )

            self.run_id = result.scalar()

        logger.info(
            f"Audit Run Started (Run ID: {self.run_id})"
        )

        return self.run_id


    # ======================================================
    # TABLE LOAD
    # ======================================================

    def log_table_load(
        self,
        table_name,
        rows_loaded,
        duration_seconds,
        status="Completed"
    ):
        """
        Record a completed table load.
        """

        with self.engine.begin() as connection:

            connection.execute(

                text(
                    """
                    INSERT INTO analytics.table_load_history
                    (
                        run_id,
                        table_name,
                        rows_loaded,
                        load_status,
                        load_duration_seconds
                    )

                    VALUES
                    (
                        :run_id,
                        :table_name,
                        :rows_loaded,
                        :status,
                        :duration
                    );
                    """
                ),

                {
                    "run_id": self.run_id,
                    "table_name": table_name,
                    "rows_loaded": rows_loaded,
                    "status": status,
                    "duration": duration_seconds
                }

            )

        logger.info(
            f"Audit Logged: {table_name}"
        )


    # ======================================================
    # DATA QUALITY
    # ======================================================

    def log_quality(
        self,
        table_name,
        row_count,
        duplicate_count,
        null_count,
        quality_score,
        validation_status="Passed"
    ):
        """
        Record data quality metrics.
        """

        with self.engine.begin() as connection:

            connection.execute(

                text(
                    """
                    INSERT INTO analytics.data_quality_audit
                    (
                        run_id,
                        table_name,
                        row_count,
                        duplicate_count,
                        null_count,
                        quality_score,
                        validation_status
                    )

                    VALUES
                    (
                        :run_id,
                        :table_name,
                        :row_count,
                        :duplicate_count,
                        :null_count,
                        :quality_score,
                        :validation_status
                    );
                    """
                ),

                {
                    "run_id": self.run_id,
                    "table_name": table_name,
                    "row_count": row_count,
                    "duplicate_count": duplicate_count,
                    "null_count": null_count,
                    "quality_score": quality_score,
                    "validation_status": validation_status
                }

            )

        logger.info(
            f"Quality Logged: {table_name}"
        )


    # ======================================================
    # FINISH PIPELINE
    # ======================================================

    def finish_run(
        self,
        total_tables,
        total_rows_loaded,
        status="Completed"
    ):
        """
        Finalize ETL run history.
        """

        end_time = datetime.now()

        duration = (
            end_time - self.start_time
        ).total_seconds()

        with self.engine.begin() as connection:

            connection.execute(

                text(
                    """
                    UPDATE analytics.etl_run_history

                    SET

                        end_time = :end_time,

                        duration_seconds = :duration,

                        status = :status,

                        total_tables = :total_tables,

                        total_rows_loaded = :total_rows

                    WHERE run_id = :run_id;
                    """
                ),

                {
                    "end_time": end_time,
                    "duration": duration,
                    "status": status,
                    "total_tables": total_tables,
                    "total_rows": total_rows_loaded,
                    "run_id": self.run_id
                }

            )

        logger.info(
            f"Audit Run Completed (Run ID: {self.run_id})"
        )