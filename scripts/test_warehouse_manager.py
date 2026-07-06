"""
Test Warehouse Manager Operations
"""

from src.core.services import ServiceContainer

services = ServiceContainer()



def main():

    warehouse = services.warehouse_manager

    print("=" * 60)
    print("Warehouse Status")
    print("=" * 60)

    print(warehouse.status())
    print()

    print("=" * 60)
    print("Refresh Metadata")
    print("=" * 60)

    result = warehouse.refresh_metadata()

    print(result)
    print()

    print("=" * 60)
    print("Warehouse Health")
    print("=" * 60)

    result = warehouse.health()

    print(result)
    print()

    print("=" * 60)
    print("Warehouse Statistics")
    print("=" * 60)

    result = warehouse.statistics()

    print(result)
    print()

    print("=" * 60)
    print("Warehouse Validation")
    print("=" * 60)

    validation = warehouse.validate()

    print(validation)


if __name__ == "__main__":
    main()