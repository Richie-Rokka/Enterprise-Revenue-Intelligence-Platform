"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : theme.py
Package     : src.presentation
Purpose     : Enterprise Presentation Theme
Author      : ERIP
Version     : 1.0.0

Description
-----------
Shared presentation constants for the Enterprise Presentation Framework.

This module defines the visual appearance of console output across
Warehouse, Semantic, Monitoring, Quality, Runtime and future frameworks.

Responsibilities
----------------
- Console width
- Borders
- Separators
- Status labels
- Symbols

===============================================================================
"""

from __future__ import annotations

# =============================================================================
# Console Layout
# =============================================================================

WIDTH = 80

BORDER = "="

SEPARATOR = "-"

# =============================================================================
# Status Labels
# =============================================================================

STATUS_SUCCESS = "SUCCESS"

STATUS_FAILED = "FAILED"

STATUS_WARNING = "WARNING"

STATUS_INFO = "INFO"

STATUS_READY = "READY"

STATUS_INVALID = "INVALID"

STATUS_HEALTHY = "HEALTHY"

STATUS_UNHEALTHY = "UNHEALTHY"

# =============================================================================
# Symbols
# =============================================================================

SUCCESS_SYMBOL = "[✓]"

FAILURE_SYMBOL = "[✗]"

WARNING_SYMBOL = "[!]"

INFO_SYMBOL = "[i]"