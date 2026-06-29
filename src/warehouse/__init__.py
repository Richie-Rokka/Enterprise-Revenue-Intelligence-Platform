"""
Enterprise Revenue Intelligence Platform (ERIP)

Warehouse Package

Provides the enterprise warehouse framework used to
build, validate, and maintain the analytical data warehouse.

Public API
----------
WarehouseManager
    Primary entry point for warehouse operations.

Example
-------
from src.warehouse import WarehouseManager

warehouse = WarehouseManager()

warehouse.rebuild()
"""

from .manager import WarehouseManager

__version__ = "2.0.0"

__all__ = [
    "WarehouseManager",
]