"""
Enterprise Revenue Intelligence Platform (ERIP)

Integration Test

Observability Package
"""

from src.observability import (
    get_logger,
    Timer,
    get_memory_usage,
    PipelineSummary,
)


def main():

    logger = get_logger(__name__)

    logger.info("=" * 60)
    logger.info("OBSERVABILITY PACKAGE TEST")
    logger.info("=" * 60)

    # -------------------------------------------------
    # Timer Test
    # -------------------------------------------------

    with Timer() as timer:

        total = 0

        for i in range(1_000_000):

            total += i

    logger.info(
        f"Timer Test Passed: "
        f"{timer.elapsed_seconds:.4f} seconds"
    )

    # -------------------------------------------------
    # Memory Test
    # -------------------------------------------------

    memory = get_memory_usage()

    logger.info(
        f"Memory Usage: "
        f"{memory.current_mb:.2f} MB"
    )

    # -------------------------------------------------
    # Pipeline Summary Test
    # -------------------------------------------------

    summary = PipelineSummary(

        pipeline_name="Observability Integration Test"

    )

    summary.rows_processed = 1_000_000

    summary.rows_loaded = 1_000_000

    summary.rows_failed = 0

    summary.execution_time_seconds = timer.elapsed_seconds

    summary.memory_usage_mb = memory.current_mb

    summary.quality_score = 100.0

    summary.mark_success()

    logger.info("")

    logger.info(summary.format())

    logger.info("")

    logger.info(
        "Observability Package Test Completed Successfully."
    )


if __name__ == "__main__":

    main()