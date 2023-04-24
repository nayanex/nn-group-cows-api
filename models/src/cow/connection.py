import os
from typing import Any, List, Optional
from urllib import parse as urllib_parse

import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy.orm import Session

db_tables: List[str] = []
db_foreign_keys: List[str] = []


def create_engine(url: Optional[str], echo: Any = None) -> Any:
    if url is None:
        url = os.getenv("SQL_URL")
        if url is None:
            raise AttributeError("No url given, please set SQL_URL env value")
    if echo is None:
        debug_env = os.getenv("DEBUG")
        echo = debug_env is not None and debug_env.lower() == "true"

    return sa.create_engine(url, echo=echo)


def create_sqlite_engine(path: str, echo: Any = None) -> Any:
    return create_engine("sqlite:///" + path, echo=echo)


def create_sqlite_in_memory_engine(echo: Any = None) -> Any:
    return create_engine("sqlite:///", echo=echo)


def create_mssql(
    hostname: str,
    database: str,
    user: str,
    password: str,
    authentication: str = "SqlPassword",
    driver: str = "ODBC Driver 17 for SQL Server",
    port: int = 1433,
    echo: Any = None,
) -> Any:
    url = f"mssql://{user}:{password}@{hostname}:{port}/{database}?driver={urllib_parse.quote_plus(driver)}"
    if authentication != "SqlPassword":
        url = url + "&Authentication=" + urllib_parse.quote_plus(authentication)
    return create_engine(url, echo=echo)


def run_migrations(dsn: str, revision: Optional[str] = None) -> None:
    global db_foreign_keys, db_tables

    if not revision:
        revision = "head"
    if "mssql" in dsn:
        # Query known foreign key and table names for MSSQL as may be required when migrating data
        engine = create_engine(dsn)
        with engine.connect() as session:
            db_tables = [
                f"{x[0]}.{x[1]}"
                for x in session.execute(
                    """
                SELECT sch.name as schema_name, tbl.name as table_name FROM sys.tables tbl
                JOIN sys.schemas sch ON sch.schema_id = tbl.schema_id
            """
                )
            ]
            db_foreign_keys = [x[0] for x in session.execute("SELECT name FROM sys.foreign_keys WHERE type='F'")]
    alembic_cfg = Config()
    script_location = os.path.dirname(__file__) + os.path.sep + "alembic"
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    command.upgrade(alembic_cfg, revision)


def clean_database(session: Session) -> None:
    path = os.path.dirname(__file__) + os.path.sep + "clean_database.sql"
    with open(path, "r") as file:
        data = file.read()
    session.execute(data)


def get_mssql_fk_name(substring: str) -> Optional[str]:
    """
    For SQL Server connections: return the first foreign key that has the given substring in its name.
    :param substring: Foreign key searched for
    :return: Actual name of foreign key. None if foreign key could not be found
    """
    for x in db_foreign_keys:
        if substring in x:
            return x
    return None
