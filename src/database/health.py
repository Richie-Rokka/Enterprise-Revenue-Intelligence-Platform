from sqlalchemy import text
from sqlalchemy.engine import Engine


class DatabaseHealth:
    """
    Enterprise Database Health Service.
    """

    def __init__(self, engine: Engine) -> None:

        self._engine = engine

    def status(self) -> str:

        return "READY" if self.check()["status"] == "Healthy" else "FAILED"

    def check(self) -> dict:

        with self._engine.connect() as connection:

            version = connection.execute(
                text("SELECT version();")
            ).scalar()

            database = connection.execute(
                text("SELECT current_database();")
            ).scalar()

            user = connection.execute(
                text("SELECT current_user;")
            ).scalar()

        return {

            "status": "Healthy",

            "database": database,

            "user": user,

            "version": version,

        }