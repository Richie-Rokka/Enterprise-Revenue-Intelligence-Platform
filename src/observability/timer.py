"""
Enterprise Revenue Intelligence Platform (ERIP)

Execution Timer

Provides a reusable context manager for measuring
execution time across ETL pipelines.
"""

from __future__ import annotations

from time import perf_counter


class Timer:
    """
    Enterprise execution timer.

    Example
    -------
    >>> with Timer() as timer:
    ...     run_pipeline()
    ...
    >>> print(timer.elapsed_seconds)
    """

    def __init__(self) -> None:
        """
        Initialize timer.
        """

        self.start_time: float | None = None
        self.end_time: float | None = None
        self.elapsed_seconds: float = 0.0

    def __enter__(self) -> "Timer":
        """
        Start timing.
        """

        self.start_time = perf_counter()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        """
        Stop timing.
        """

        self.end_time = perf_counter()

        self.elapsed_seconds = (
            self.end_time
            - self.start_time
        )

    @property
    def elapsed_milliseconds(self) -> float:
        """
        Execution time in milliseconds.
        """

        return self.elapsed_seconds * 1000

    @property
    def elapsed_minutes(self) -> float:
        """
        Execution time in minutes.
        """

        return self.elapsed_seconds / 60

    def reset(self) -> None:
        """
        Reset timer.
        """

        self.start_time = None
        self.end_time = None
        self.elapsed_seconds = 0.0