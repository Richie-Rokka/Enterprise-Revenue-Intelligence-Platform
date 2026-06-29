"""
Enterprise Revenue Intelligence Platform (ERIP)

Warehouse Registry

Defines the execution manifest for all warehouse
DDL scripts.

The registry provides a deterministic execution
order for warehouse deployment.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.config.config import config


@dataclass(frozen=True, slots=True)
class SQLScript:
    """
    Represents a deployable SQL script.
    """

    order: int

    filename: str

    category: str

    description: str

    enabled: bool = True

    @property
    def path(self) -> Path:
        """
        Return the full path to the SQL file.
        """

        project_root = Path(__file__).resolve().parents[2]

        return (
            project_root
            / "sql"
            / self.category
            / self.filename
        )


class DDLRegistry:
    """
    Enterprise Warehouse DDL Registry.
    """

    def __init__(self) -> None:

        self._scripts = [

            SQLScript(
                1,
                "001_create_schemas.sql",
                "ddl",
                "Create database schemas",
            ),

            SQLScript(
                2,
                "002_create_staging.sql",
                "ddl",
                "Create staging tables",
            ),

            SQLScript(
                3,
                "003_create_dimensions.sql",
                "ddl",
                "Create dimension tables",
            ),

            SQLScript(
                4,
                "004_create_facts.sql",
                "ddl",
                "Create fact tables",
            ),

            SQLScript(
                5,
                "005_create_indexes.sql",
                "ddl",
                "Create indexes",
            ),

            SQLScript(
                6,
                "006_create_constraints.sql",
                "ddl",
                "Create constraints",
            ),

            SQLScript(
                7,
                "007_create_views.sql",
                "ddl",
                "Create analytical views",
            ),

            SQLScript(
                8,
                "008_seed_reference_data.sql",
                "ddl",
                "Seed reference tables",
            ),
        ]

    def all(self) -> list[SQLScript]:
        """
        Return all enabled scripts ordered by execution.
        """

        return sorted(

            (
                script
                for script in self._scripts
                if script.enabled
            ),

            key=lambda script: script.order,
        )

    def categories(self) -> list[str]:
        """
        Return registered categories.
        """

        return sorted(

            {

                script.category

                for script in self._scripts

            }

        )

    def validate(self) -> None:
        """
        Validate registry integrity.
        """

        orders = [

            script.order

            for script in self._scripts

        ]

        if len(orders) != len(set(orders)):

            raise ValueError(
                "Duplicate execution order detected."
            )

        filenames = [

            script.filename

            for script in self._scripts

        ]

        if len(filenames) != len(set(filenames)):

            raise ValueError(
                "Duplicate SQL filename detected."
            )

        missing = [

            script.path

            for script in self._scripts

            if not script.path.exists()

        ]

        if missing:

            missing_files = "\n".join(

                str(path)

                for path in missing

            )

            raise FileNotFoundError(

                "Missing SQL scripts:\n"

                f"{missing_files}"

            )

    def __iter__(self):
        """
        Iterate over registered scripts.
        """

        return iter(self.all())

    def __len__(self) -> int:
        """
        Number of enabled scripts.
        """

        return len(self.all())