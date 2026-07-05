"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : registry.py
Package     : src.quality
Purpose     : Enterprise Data Quality Registry
Author      : ERIP
Version     : 2.0.0

Description
-----------
Discovers, validates and registers SQL assets used by the Enterprise
Data Quality Framework.

Responsibilities
----------------
- Discover quality SQL scripts
- Validate quality assets
- Provide execution order
- Expose registry summary

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from src.observability import get_logger


logger = get_logger(__name__)


# =============================================================================
# Quality Asset
# =============================================================================


@dataclass(slots=True)
class QualityAsset:
    """
    Enterprise Data Quality SQL asset.
    """

    name: str

    path: Path

    group: str

    @property
    def filename(self) -> str:
        """
        SQL filename.
        """

        return self.path.name


# =============================================================================
# Quality Registry
# =============================================================================


class QualityRegistry:
    """
    Enterprise Data Quality Registry.
    """

    ROOT = Path(__file__).resolve().parents[2]

    SQL_ROOT = ROOT / "sql"

    DEPLOYMENT_ORDER = (

        "quality",

        "operations",

    )

    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self._assets = self._discover()

    # -------------------------------------------------------------------------

    def _discover(self) -> list[QualityAsset]:
        """
        Discover quality SQL assets.
        """

        assets: list[QualityAsset] = []

        for group in self.DEPLOYMENT_ORDER:

            folder = self.SQL_ROOT / group

            if not folder.exists():

                logger.info(

                    "Quality folder not found: %s",

                    folder,

                )

                continue

            sql_files = sorted(

                folder.glob("*.sql")

            )

            for sql in sql_files:

                assets.append(

                    QualityAsset(

                        name=sql.stem,

                        path=sql,

                        group=group,

                    )

                )

        logger.info(

            "Discovered %s quality assets.",

            len(assets),

        )

        return assets

    # -------------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate registry integrity.
        """

        missing_assets = [

            asset.path

            for asset in self._assets

            if not asset.path.exists()

        ]

        if missing_assets:

            raise FileNotFoundError(

                "Missing quality SQL assets:\n"

                + "\n".join(

                    str(path)

                    for path in missing_assets

                )

            )

        logger.info(

            "Quality Registry Validated (%s assets)",

            len(self._assets),

        )

    # -------------------------------------------------------------------------

    def summary(self) -> dict[str, int]:
        """
        Registry summary.
        """

        summary: dict[str, int] = {}

        for group in self.DEPLOYMENT_ORDER:

            summary[group] = sum(

                1

                for asset in self._assets

                if asset.group == group

            )

        return summary

    # -------------------------------------------------------------------------

    @property
    def assets(self) -> list[QualityAsset]:
        """
        Registered quality assets.
        """

        return self._assets.copy()

    # -------------------------------------------------------------------------

    def assets_by_group(
        self,
        group: str,
    ) -> list[QualityAsset]:
        """
        Return assets for a specific group.
        """

        return [

            asset

            for asset in self._assets

            if asset.group == group

        ]

    # -------------------------------------------------------------------------

    def find(
        self,
        name: str,
    ) -> QualityAsset | None:
        """
        Find an asset by name.
        """

        for asset in self._assets:

            if asset.name == name:

                return asset

        return None

    # -------------------------------------------------------------------------

    def __iter__(self) -> Iterator[QualityAsset]:

        return iter(self._assets)

    # -------------------------------------------------------------------------

    def __len__(self) -> int:

        return len(self._assets)