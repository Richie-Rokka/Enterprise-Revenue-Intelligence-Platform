"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : registry.py
Package     : src.semantic
Purpose     : Dependency-aware Semantic Registry
Author      : ERIP
Version     : 2.2.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from graphlib import TopologicalSorter
from pathlib import Path

from src.observability import get_logger


logger = get_logger(__name__)

ROOT = Path(__file__).resolve().parents[2]
VIEWS_DIR = ROOT / "sql" / "views"


# =============================================================================
# Semantic Script
# =============================================================================

@dataclass(slots=True)
class SemanticScript:

    name: str

    path: Path


# =============================================================================
# Semantic Registry
# =============================================================================

class SemanticRegistry:
    """
    Enterprise dependency-aware Semantic Registry.
    """

    # -------------------------------------------------------------------------
    # File Locations
    # -------------------------------------------------------------------------

    FILES = {

        "vw_sales":
        "analytics/vw_sales.sql",

        "vw_customer_sales":
        "analytics/vw_customer_sales.sql",

        "vw_product_performance":
        "analytics/vw_product_performance.sql",

        "vw_seller_performance":
        "analytics/vw_seller_performance.sql",

        "vw_revenue_dashboard":
        "analytics/vw_revenue_dashboard.sql",

    }

    # -------------------------------------------------------------------------
    # Dependency Graph
    # -------------------------------------------------------------------------

    DEPENDENCIES = {

        "vw_sales": [],

        "vw_customer_sales": [
        "vw_sales",
        ],

        "vw_product_performance": [
        "vw_sales",
        ],

        "vw_seller_performance": [
        "vw_sales",
        ],

        "vw_revenue_dashboard": [
        "vw_sales",
        ],
    }

    # -------------------------------------------------------------------------

    def __init__(self):

        order = self._deployment_order()

        self._scripts = [

            SemanticScript(

                name=view,

                path=VIEWS_DIR / self.FILES[view],

            )

            for view in order

        ]

    # -------------------------------------------------------------------------

    def _deployment_order(self) -> list[str]:
        """
        Compute dependency order.
        """

        sorter = TopologicalSorter()

        for view, dependencies in self.DEPENDENCIES.items():

            sorter.add(

                view,

                *dependencies,

            )

        return list(sorter.static_order())

    # -------------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate semantic assets.
        """

        missing = [

            script.path

            for script in self._scripts

            if not script.path.exists()

        ]

        if missing:

            raise FileNotFoundError(

                "Missing semantic SQL scripts:\n"

                + "\n".join(

                    str(path)

                    for path in missing

                )

            )

        logger.info(

            "Semantic Registry Validated (%d scripts)",

            len(self._scripts),

        )

    # -------------------------------------------------------------------------

    @property
    def paths(self) -> list[Path]:

        return [

            script.path

            for script in self._scripts

        ]

    # -------------------------------------------------------------------------

    def __iter__(self):

        return iter(self._scripts)

    def __len__(self):

        return len(self._scripts)