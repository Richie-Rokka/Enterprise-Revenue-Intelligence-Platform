"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : registry.py
Package     : src.semantic
Purpose     : Semantic Layer SQL Registry
Author      : ERIP
Version     : 2.0.0

Description
-----------
Discovers, validates and registers all SQL view scripts that make up the
Enterprise Semantic Layer.

Deployment Order
----------------
Semantic
    ↓
Operational
    ↓
Analytics
    ↓
Executive

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from src.observability import get_logger


logger = get_logger(__name__)


# =============================================================================
# SQL SCRIPT
# =============================================================================


@dataclass(slots=True)
class SQLScript:
    """
    Semantic SQL deployment script.
    """

    name: str

    path: Path

    group: str

    @property
    def filename(self) -> str:

        return self.path.name


# =============================================================================
# REGISTRY
# =============================================================================


class SemanticRegistry:
    """
    Enterprise Semantic Registry.
    """

    ROOT = Path(__file__).resolve().parents[2]

    SQL_ROOT = ROOT / "sql" / "views"

    DEPLOYMENT_ORDER = (

        "semantic",

        "operational",

        "analytics",

        "executive",

    )

    def __init__(self) -> None:

        self._scripts = self._discover()

    # -------------------------------------------------------------------------

    def _discover(self) -> list[SQLScript]:
        """
        Discover semantic SQL files.
        """

        scripts: list[SQLScript] = []

        for group in self.DEPLOYMENT_ORDER:

            folder = self.SQL_ROOT / group

            if not folder.exists():

                logger.warning(

                    "Semantic folder not found: %s",

                    folder,

                )

                continue

            sql_files = sorted(

                folder.glob("*.sql")

            )

            for sql in sql_files:

                scripts.append(

                    SQLScript(

                        name=sql.stem,

                        path=sql,

                        group=group,

                    )

                )

        return scripts

    # -------------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate registry.
        """

        missing_folders = []

        for group in self.DEPLOYMENT_ORDER:

            folder = self.SQL_ROOT / group

            if not folder.exists():

                missing_folders.append(folder)

        if missing_folders:

            raise FileNotFoundError(

                "Missing Semantic folders:\n"

                + "\n".join(

                    str(folder)

                    for folder in missing_folders

                )

            )

        missing_scripts = [

            script.path

            for script in self._scripts

            if not script.path.exists()

        ]

        if missing_scripts:

            raise FileNotFoundError(

                "Missing Semantic SQL:\n"

                + "\n".join(

                    str(path)

                    for path in missing_scripts

                )

            )

        logger.info(

            "Semantic Registry Validated (%s scripts)",

            len(self._scripts),

        )

    # -------------------------------------------------------------------------

    def __iter__(self) -> Iterator[SQLScript]:

        return iter(self._scripts)

    # -------------------------------------------------------------------------

    def __len__(self) -> int:

        return len(self._scripts)

    # -------------------------------------------------------------------------

    @property
    def scripts(self) -> list[SQLScript]:

        return self._scripts.copy()

    # -------------------------------------------------------------------------

    def summary(self) -> dict[str, int]:
        """
        Deployment summary.
        """

        return {

            group: len(

                [

                    script

                    for script in self._scripts

                    if script.group == group

                ]

            )

            for group in self.DEPLOYMENT_ORDER

        }