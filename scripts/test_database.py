from pprint import pprint

from src.database import check_database_health

pprint(
    check_database_health()
)