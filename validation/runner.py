"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    runner.py

Purpose:
    Enterprise Validation Framework Runner

Description:
    Executes all ERIP validators in dependency order and produces
    an enterprise validation report.

Responsibilities
----------------
• Execute validators
• Capture execution time
• Continue after validator failures
• Produce execution summary
• Return operating system exit code

Author:
    Abodunrin Oketade

Platform:
    Enterprise Revenue Intelligence Platform (ERIP)

Version:
    2.1.0
===============================================================================
"""

from __future__ import annotations

import sys
import time
from typing import List

from .models import ValidationResult
from .models import ValidationSummary

from .test_database import DatabaseValidator
from .test_schemas import SchemaValidator
from .test_metadata import MetadataValidator
from .test_reference_data import ReferenceDataValidator
from .test_staging_tables import StagingValidator
from .test_constraints import ConstraintValidator
from .test_indexes import IndexValidator
from .test_warehouse import WarehouseValidator


# ==============================================================================
# VALIDATION RUNNER
# ==============================================================================


class ValidationRunner:
    """
    Executes the complete ERIP Validation Framework.
    """

    def __init__(self):

        self.validators = [

            DatabaseValidator(),

            SchemaValidator(),

            MetadataValidator(),

            ReferenceDataValidator(),

            StagingValidator(),

            ConstraintValidator(),

            IndexValidator(),

            WarehouseValidator(),

        ]

        self.results: List[ValidationResult] = []

    # -------------------------------------------------------------------------

    def run(self) -> int:

        """
        Execute all validators.

        Returns
        -------
        int

            0 -> Success

            1 -> Failure
        """

        self.results.clear()

        self._print_header()

        start = time.perf_counter()

        for validator in self.validators:

            validator_start = time.perf_counter()

            try:

                result = validator.validate()

            except Exception as exc:

                result = ValidationResult(

                    name=validator.NAME,

                    passed=False,

                    message=f"{type(exc).__name__}: {exc}",

                )

            result.duration = (

                time.perf_counter()

                - validator_start

            )

            self.results.append(result)

            self._print_result(result)

        total_duration = (

            time.perf_counter()

            - start

        )

        summary = self._build_summary(

            total_duration

        )

        self._print_summary(summary)

        return 0 if summary.success else 1

    # -------------------------------------------------------------------------

    def _build_summary(

        self,

        duration: float,

    ) -> ValidationSummary:

        passed = sum(

            result.passed

            for result in self.results

        )

        failed = len(self.results) - passed

        return ValidationSummary(

            total=len(self.results),

            passed=passed,

            failed=failed,

            duration=duration,

            success=failed == 0,

        )

    # -------------------------------------------------------------------------

    @staticmethod
    def _print_header():

        print()

        print("=" * 78)

        print("ERIP VALIDATION FRAMEWORK")

        print("=" * 78)

        print()

    # -------------------------------------------------------------------------

    @staticmethod
    def _print_result(

        result: ValidationResult,

    ):

        status = "PASS" if result.passed else "FAIL"

        print(

            f"{result.name:.<48}"

            f"{status}"

            f" ({result.duration:.3f}s)"

        )

        if result.message:

            print(

                f"    {result.message}"

            )

    # -------------------------------------------------------------------------

    @staticmethod
    def _print_summary(

        summary: ValidationSummary,

    ):

        print()

        print("=" * 78)

        print("VALIDATION SUMMARY")

        print("-" * 78)

        print(

            f"Validators Executed : "

            f"{summary.total}"

        )

        print(

            f"Passed              : "

            f"{summary.passed}"

        )

        print(

            f"Failed              : "

            f"{summary.failed}"

        )

        print(

            f"Execution Time      : "

            f"{summary.duration:.2f} seconds"

        )

        print("=" * 78)

        print()

        if summary.success:

            print(

                "✓ ERIP Validation Successful"

            )

        else:

            print(

                "✗ ERIP Validation Failed"

            )

        print()


# ==============================================================================
# ENTRY POINT
# ==============================================================================


def main():

    """
    Framework entry point.
    """

    runner = ValidationRunner()

    sys.exit(

        runner.run()

    )


if __name__ == "__main__":

    main()