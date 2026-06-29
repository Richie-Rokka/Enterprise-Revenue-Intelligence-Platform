"""
Enterprise Revenue Intelligence Platform (ERIP)

Central Configuration Manager

Loads all YAML configuration files and exposes
them through a single Config object.
"""

from pathlib import Path
from types import SimpleNamespace

import yaml


ROOT_DIR = Path(__file__).resolve().parents[2]

CONFIG_DIR = ROOT_DIR / "config"


def _to_namespace(data):
    """
    Recursively convert dictionaries into objects.

    Example:

    config.database.host
    """

    if isinstance(data, dict):

        return SimpleNamespace(
            **{
                key: _to_namespace(value)
                for key, value in data.items()
            }
        )

    if isinstance(data, list):

        return [
            _to_namespace(item)
            for item in data
        ]

    return data


def _load_yaml(filename):
    """
    Load a YAML configuration file.
    """

    path = CONFIG_DIR / filename

    if not path.exists():

        raise FileNotFoundError(
            f"Missing configuration file: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:

        return yaml.safe_load(file)


class Config:

    """
    Central configuration object.
    """

    def __init__(self):

        self.database = _to_namespace(
            _load_yaml("database.yaml")["database"]
        )

        self.logging = _to_namespace(
            _load_yaml("logging.yaml")["logging"]
        )

        self.pipeline = _to_namespace(
            _load_yaml("pipeline.yaml")["pipeline"]
        )

        self.quality = _to_namespace(
            _load_yaml("quality.yaml")["quality"]
        )


config = Config()