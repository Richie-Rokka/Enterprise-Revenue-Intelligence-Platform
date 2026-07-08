"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Package     : src.presentation
Purpose     : Enterprise Presentation Framework

Author      : ERIP
Version     : 3.0.0

Description
-----------
Public API for the Enterprise Presentation Framework.

Provides presentation services used throughout the Enterprise Revenue
Intelligence Platform.

Framework Components
--------------------
Infrastructure
- Console
- Formatter
- Report
- BasePresenter

Presenters
----------
- RuntimePresenter
- WarehousePresenter
- SemanticPresenter

Future Presenters
-----------------
- MonitoringPresenter
- QualityPresenter

===============================================================================
"""

from .base_presenter import BasePresenter

from .console import Console
from .formatter import Formatter
from .report import Report

from .runtime_presenter import RuntimePresenter
from .warehouse_presenter import WarehousePresenter
from .semantic_presenter import SemanticPresenter
from .monitoring_presenter import MonitoringPresenter
from .quality_presenter import QualityPresenter


__all__ = [

    # Infrastructure

    "BasePresenter",

    "Console",

    "Formatter",

    "Report",

    # Presenters

    "RuntimePresenter",

    "WarehousePresenter",

    "SemanticPresenter",

    "MonitoringPresenter",

    "QualityPresenter",

]