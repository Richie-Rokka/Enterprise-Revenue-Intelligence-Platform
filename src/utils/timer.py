"""
timer.py
Enterprise Revenue Intelligence Platform

Reusable execution timer.
"""

from time import perf_counter


class Timer:
    """
    Simple execution timer.

    Supports both manual timing and
    Python's context manager syntax.

    Example
    -------
    Manual:

        timer = Timer()
        timer.start()

        ...

        timer.stop()

        print(timer.elapsed)

    Context Manager:

        with Timer() as timer:

            ...

        print(timer.elapsed)
    """

    def __init__(self):

        self.start_time = None
        self.end_time = None

    # ======================================================
    # Manual Timing
    # ======================================================

    def start(self):

        self.start_time = perf_counter()

    def stop(self):

        self.end_time = perf_counter()

    # ======================================================
    # Context Manager
    # ======================================================

    def __enter__(self):

        self.start()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):

        self.stop()

        # Returning False ensures any exception
        # is re-raised normally.
        return False

    # ======================================================
    # Elapsed Time
    # ======================================================

    @property
    def elapsed(self):

        if self.start_time is None:
            return 0.0

        end = self.end_time or perf_counter()

        return round(
            end - self.start_time,
            2
        )