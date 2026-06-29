"""
Enterprise Revenue Intelligence Platform (ERIP)

Database Connection Manager

Responsible for:

- Creating SQLAlchemy engine
- Managing connection pooling
- Providing database connections
"""

from sqlalchemy import create_engine

from src.config.config import config


_ENGINE = None


def build_connection_string():
    """
    Build the SQLAlchemy connection string.
    """

    database = config.database

    return (
        f"{database.driver}://"
        f"{database.username}:"
        f"{database.password}@"
        f"{database.host}:"
        f"{database.port}/"
        f"{database.database}"
    )


def get_engine():
    """
    Return a singleton SQLAlchemy engine.
    """

    global _ENGINE

    if _ENGINE is None:

        database = config.database

        _ENGINE = create_engine(

            build_connection_string(),

            pool_size=database.connection.pool_size,

            max_overflow=database.connection.max_overflow,

            pool_timeout=database.connection.pool_timeout,

            pool_recycle=database.connection.pool_recycle,

            future=True,
        )

    return _ENGINE


def get_connection():
    """
    Return an active database connection.
    """

    return get_engine().connect()