"""db.py - provide methods related to the database interface."""
import logging
import os
from contextlib import contextmanager
from typing import Any, Dict
from urllib import parse as urllib_parse

import sqlalchemy as sa
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from . import app_config

sqlite_schemas = {}

SQLITE_PATH_EMR = os.getenv("SQLITE_PATH_COW")
SQL_COPT_SS_ACCESS_TOKEN = 1256
DATABASE_ACCESS_TOKEN_URL = "https://database.windows.net/"  # nosec


def sa_url() -> str:
    """Returns url to access the supported database either SQLSERVER or SQLITE"""
    protocol = app_config.sql_protocol()
    if protocol == "sqlite":
        if "emr" not in sqlite_schemas:
            if SQLITE_PATH_EMR is None:
                raise RuntimeError("SQLITE_EMR_PATH is missing in env")
            sqlite_schemas["emr"] = SQLITE_PATH_EMR
        return "sqlite://"
    elif protocol == "mssql":
        url = app_config.sql_protocol() + "://"
        if app_config.sql_authentication() == "SqlPassword":
            url = url + f"{app_config.sql_user()}:{app_config.sql_pass()}@"
        url = (
            url
            + app_config.sql_server()
            + "/"
            + app_config.sql_db()
            + "?driver="
            + urllib_parse.quote_plus(app_config.odbc_driver())
        )
        if app_config.sql_authentication() != "SqlPassword":
            url = url + "&Authentication=" + urllib_parse.quote_plus(app_config.sql_authentication())
        if app_config.sql_authentication() != "ActiveDirectoryMsi" and app_config.sql_authentication() != "SqlPassword":
            url = (
                url
                + "&user="
                + urllib_parse.quote_plus(app_config.sql_user())
                + "&password="
                + urllib_parse.quote_plus(app_config.sql_pass())
            )
        return url
    elif protocol == "msimssql":
        url = urllib_parse.quote_plus(
            f"Driver={{{app_config.odbc_driver()}}}"
            + f";Server=tcp:{app_config.sql_server()}"
            + f";Database={app_config.sql_db()}"
        )
        url = f"mssql+pyodbc:///?odbc_connect={url}"
        return url
    else:
        raise AttributeError("Only sqlite, mssql and msimssql are supported")


def engine() -> Any:
    """Helper function to create a SqlAlchemy engine"""
    connect_args: Dict[str, Any] = {"check_same_thread": False}

    protocol = app_config.sql_protocol()
    try:
        _engine = sa.create_engine(sa_url(), connect_args=connect_args)
    except Exception as e:
        logging.exception(e)
        raise e
    if protocol == "sqlite":
        for key, path in sqlite_schemas.items():
            _engine.execute(f"attach database '{path}' as {key}")
    return _engine


def local_db_only() -> bool:
    """Determines whether engine is a local database or not.
    Used as a safeguard for destructive database operations"""
    return (
        "localhost" in app_config.sql_server()
        or "127.0.0.1" in app_config.sql_server()
        or "0.0.0.0" in app_config.sql_server()
    )


@contextmanager
def create_session() -> Session:
    """Creates a database session using given configuration"""

    sm = scoped_session(sessionmaker(bind=engine()))
    session = sm()
    try:
        yield session
        session.commit()
    except:  # noqa: E722
        session.rollback()
        raise
    finally:
        session.close()
