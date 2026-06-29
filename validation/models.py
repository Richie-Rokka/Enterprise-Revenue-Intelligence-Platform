"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)

Module:
    models.py

Purpose:
    Shared models used throughout the ERIP Validation Framework.

Description:
    Defines immutable data structures exchanged between validators and the
    validation runner.

Design Principles
-----------------
• Framework-wide contracts
• No database dependencies
• No business logic
• No side effects

Author:
    Abodunrin Oketade

Platform:
    Enterprise Revenue Intelligence Platform (ERIP)

Version:
    2.1.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# ==============================================================================
# VALIDATION RESULT
# ==============================================================================

@dataclass(slots=True)
class ValidationResult:
    """
    Represents the result of a single validator execution.
    """

    name: str

    passed: bool

    message: str = ""

    duration: float = 0.0

    timestamp: datetime = datetime.now()


# ==============================================================================
# VALIDATION SUMMARY
# ==============================================================================

@dataclass(slots=True)
class ValidationSummary:
    """
    Represents the complete validation execution.
    """

    total: int

    passed: int

    failed: int

    duration: float

    success: bool


# ==============================================================================
# VALIDATION CONSTANTS
# ==============================================================================

PASS = "PASS"

FAIL = "FAIL"

SUCCESS = True

FAILED = False

FRAMEWORK_NAME = "ERIP Validation Framework"

FRAMEWORK_VERSION = "2.1.0"