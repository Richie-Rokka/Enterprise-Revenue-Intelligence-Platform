"""
Enterprise Revenue Intelligence Platform (ERIP)

Pipeline Summary

Provides a standardized execution summary for all
ETL pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class PipelineSummary:
    """
    Standard execution summary for an ETL pipeline.
    """

    pipeline_name: str

    status: str = "RUNNING"

    start_time: datetime = field(
        default_factory=datetime.now
    )

    end_time: datetime | None = None

    execution_time_seconds: float = 0.0

    rows_processed: int = 0

    rows_loaded: int = 0

    rows_failed: int = 0

    memory_usage_mb: float = 0.0

    quality_score: float | None = None

    error_message: str | None = None

    def mark_success(self) -> None:
        """
        Mark pipeline as successful.
        """

        self.status = "SUCCESS"

        self.end_time = datetime.now()

    def mark_failed(
        self,
        message: str,
    ) -> None:
        """
        Mark pipeline as failed.
        """

        self.status = "FAILED"

        self.error_message = message

        self.end_time = datetime.now()

    def format(self) -> str:
        """
        Return a formatted pipeline summary.
        """

        lines = [

            "=" * 60,

            f"Pipeline : {self.pipeline_name}",

            "=" * 60,

            f"Status                : {self.status}",

            f"Rows Processed        : {self.rows_processed:,}",

            f"Rows Loaded           : {self.rows_loaded:,}",

            f"Rows Failed           : {self.rows_failed:,}",

            f"Execution Time (sec)  : {self.execution_time_seconds:.2f}",

            f"Memory Usage (MB)     : {self.memory_usage_mb:.2f}",
        ]

        if self.quality_score is not None:

            lines.append(
                f"Quality Score (%)     : {self.quality_score:.2f}"
            )

        if self.error_message:

            lines.append(
                f"Error                 : {self.error_message}"
            )

        lines.append("=" * 60)

        return "\n".join(lines)