"""
Enterprise Revenue Intelligence Platform (ERIP)

Database Health Check
"""

from sqlalchemy import text

from src.database.connection import get_engine


def check_database_health():
    """
    Perform a database health check.

    Returns
    -------
    dict
        Database health information.
    """

    engine = get_engine()

    with engine.connect() as connection:

        version = connection.execute(

            text(
                "SELECT version();"
            )

        ).scalar()

        database = connection.execute(

            text(
                "SELECT current_database();"
            )

        ).scalar()

        user = connection.execute(

            text(
                "SELECT current_user;"
            )

        ).scalar()

    return {

        "status": "Healthy",

        "database": database,

        "user": user,

        "version": version,
    }