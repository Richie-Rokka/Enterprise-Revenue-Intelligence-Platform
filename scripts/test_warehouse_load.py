from pprint import pprint

from src.warehouse.manager import WarehouseManager

manager = WarehouseManager()

result = manager.load()

pprint(result)