"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : registry.py
Package     : src.warehouse
Purpose     : Enterprise Warehouse SQL Registry
Author      : ERIP
Version     : 2.2.0

Description
-----------
Registers, validates and orders SQL deployment scripts for the
Enterprise Revenue Intelligence Platform (ERIP).

The registry discovers SQL deployment files automatically and returns
them in dependency order.

Only required deployment folders are enforced during validation.
Optional deployment folders are discovered when present.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from src.observability import get_logger

logger = get_logger(__name__)


# =============================================================================
# SQL Script
# =============================================================================

@dataclass(slots=True)
class SQLScript:
    """
    SQL deployment script.
    """

    name: str

    path: Path

    group: str

    @property
    def filename(self) -> str:
        return self.path.name


# =============================================================================
# Registry
# =============================================================================

class DDLRegistry:
    """
    Enterprise Warehouse SQL Registry.

    Discovers SQL deployment scripts and exposes them in dependency order.
    """

    ROOT = Path(__file__).resolve().parents[2]

    SQL_ROOT = ROOT / "sql" / "ddl"

    # -------------------------------------------------------------------------
    # Required deployment folders
    # -------------------------------------------------------------------------

    REQUIRED_GROUPS = (
        "schemas",
        "staging",
        "metadata",
        "dimensions",
    )

    # -------------------------------------------------------------------------
    # Optional deployment folders
    # -------------------------------------------------------------------------

    OPTIONAL_GROUPS = (
        "facts",
        "indexes",
        "constraints",
    )

    # -------------------------------------------------------------------------

    DEPLOYMENT_ORDER = REQUIRED_GROUPS + OPTIONAL_GROUPS

    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self._scripts = self._discover()

    # -------------------------------------------------------------------------

    def _discover(self) -> list[SQLScript]:
        """
        Discover deployment SQL scripts.
        """

        scripts: list[SQLScript] = []

        for group in self.DEPLOYMENT_ORDER:

            folder = self.SQL_ROOT / group

            if not folder.exists():

                if group in self.REQUIRED_GROUPS:

                    logger.error(
                        "Required deployment folder not found: %s",
                        folder,
                    )

                else:

                    logger.debug(
                        "Optional deployment folder not found: %s",
                        folder,
                    )

                continue

            sql_files = sorted(folder.glob("*.sql"))

            for sql in sql_files:

                scripts.append(

                    SQLScript(

                        name=sql.stem,

                        path=sql,

                        group=group,

                    )

                )

        logger.info(
            "Discovered %s deployment SQL scripts.",
            len(scripts),
        )

        return scripts

    # -------------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate deployment registry.
        """

        missing_folders: list[Path] = []

        for group in self.REQUIRED_GROUPS:

            folder = self.SQL_ROOT / group

            if not folder.exists():

                missing_folders.append(folder)

        if missing_folders:

            raise FileNotFoundError(

                "Missing required SQL deployment folders:\n"

                + "\n".join(

                    str(path)

                    for path in missing_folders

                )

            )

        missing_scripts = [

            script.path

            for script in self._scripts

            if not script.path.exists()

        ]

        if missing_scripts:

            raise FileNotFoundError(

                "Missing SQL deployment scripts:\n"

                + "\n".join(

                    str(path)

                    for path in missing_scripts

                )

            )

        logger.info(

            "Warehouse Registry Validated (%s scripts)",

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

    def summary(self) -> dict:
        """
        Return registry summary.
        """

        return {

            "required_groups": len(self.REQUIRED_GROUPS),

            "optional_groups": len(self.OPTIONAL_GROUPS),

            "registered_scripts": len(self._scripts),

            "groups": {

                group: sum(

                    script.group == group

                    for script in self._scripts

                )

                for group in self.DEPLOYMENT_ORDER

            },

        }