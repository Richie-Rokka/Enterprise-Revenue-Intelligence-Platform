"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : registry.py
Package     : src.monitoring
Purpose     : Enterprise Monitoring Registry
Author      : ERIP
Version     : 2.0.0

Description
-----------
Discovers, validates and registers SQL assets used by the Enterprise
Monitoring Framework.

Responsibilities
----------------
- Discover monitoring SQL scripts
- Validate monitoring assets
- Provide deployment order
- Expose monitoring registry summary

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from src.observability import get_logger


logger = get_logger(__name__)


# =============================================================================
# Monitoring Asset
# =============================================================================


@dataclass(slots=True)
class MonitoringAsset:
    """
    Monitoring SQL asset.
    """

    name: str

    path: Path

    group: str

    @property
    def filename(self) -> str:
        return self.path.name


# =============================================================================
# Monitoring Registry
# =============================================================================


class MonitoringRegistry:
    """
    Enterprise Monitoring Registry.
    """

    ROOT = Path(__file__).resolve().parents[2]

    SQL_ROOT = ROOT / "sql"

    DEPLOYMENT_ORDER = (
        "operations",
        "monitoring",
    )

    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self._assets = self._discover()

    # -------------------------------------------------------------------------

    def _discover(self) -> list[MonitoringAsset]:
        """
        Discover monitoring SQL assets.
        """

        assets: list[MonitoringAsset] = []

        for group in self.DEPLOYMENT_ORDER:

            folder = self.SQL_ROOT / group

            if not folder.exists():

                logger.info(

                    "Monitoring folder not found: %s",

                    folder,

                )

                continue

            sql_files = sorted(

                folder.glob("*.sql")

            )

            for sql in sql_files:

                assets.append(

                    MonitoringAsset(

                        name=sql.stem,

                        path=sql,

                        group=group,

                    )

                )

        logger.info(

            "Discovered %s monitoring assets.",

            len(assets),

        )

        return assets

    # -------------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate monitoring registry.
        """

        missing = [

            asset.path

            for asset in self._assets

            if not asset.path.exists()

        ]

        if missing:

            raise FileNotFoundError(

                "Missing monitoring SQL assets:\n"

                + "\n".join(

                    str(path)

                    for path in missing

                )

            )

        logger.info(

            "Monitoring Registry Validated (%s assets)",

            len(self._assets),

        )

    # -------------------------------------------------------------------------

    def summary(self) -> dict[str, int]:
        """
        Registry summary.
        """

        summary: dict[str, int] = {}

        for group in self.DEPLOYMENT_ORDER:

            summary[group] = len(

                [

                    asset

                    for asset in self._assets

                    if asset.group == group

                ]

            )

        return summary

    # -------------------------------------------------------------------------

    @property
    def assets(self) -> list[MonitoringAsset]:

        return self._assets.copy()

    # -------------------------------------------------------------------------

    def __iter__(self) -> Iterator[MonitoringAsset]:

        return iter(self._assets)

    # -------------------------------------------------------------------------

    def __len__(self) -> int:

        return len(self._assets)