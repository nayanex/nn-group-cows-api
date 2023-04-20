"""app_config.py - Reads the environment variables and sets the application constants."""
import os
from typing import Optional

_sql_protocol = os.getenv("SQL_PROTOCOL")
if _sql_protocol is None:
    _sql_protocol = os.getenv("APPSETTING_SQL_PROTOCOL")

_sql_server = os.getenv("SQL_SERVER")
if _sql_server is None:
    _sql_server = os.getenv("APPSETTING_SQL_SERVER")

_sql_db = os.getenv("SQL_DB")
if _sql_db is None:
    _sql_db = os.getenv("APPSETTING_SQL_DB")

_sql_authentication: str = (
    os.getenv("SQL_AUTHENTICATION") or os.getenv("APPSETTING_SQL_AUTHENTICATION") or "ActiveDirectoryPassword"
)

_sql_user = os.getenv("SQL_USER")
if _sql_user is None:
    _sql_user = os.getenv("APPSETTING_SQL_USER")

_sql_pass = os.getenv("SQL_PASS")
if _sql_pass is None:
    _sql_pass = os.getenv("CUSTOMCONNSTR_SQL_PASS")

_commit_id = os.getenv("COMMIT_ID")
_build_id = os.getenv("BUILD_ID")
_token_cache_dir = os.getenv("TOKEN_CACHE_DIR")

_odbc_driver: str = os.getenv("ODBC_DRIVER") or "ODBC Driver 17 for SQL Server"


def odbc_driver() -> str:
    """Returns a value of ODBC_DRIVER environment variable which is used for setting sql_db variables"""
    return _odbc_driver


def debug() -> bool:
    """Debug mode enabled for FastAPI with value of DEBUG environment variable if set or else True"""
    return (os.getenv("DEBUG") or "false").lower() == "true"


def sql_protocol() -> str:
    """Checks and returns the required SQL_PROTOCOL environment variable"""
    if _sql_protocol is None:
        raise AttributeError("No protocol given, please set SQL_PROTOCOL env value")
    return _sql_protocol


def sql_server() -> str:
    """Checks and returns the required SQL_SERVER environment variable"""
    if _sql_server is None:
        raise AttributeError("Please set SQL_SERVER env value")
    return _sql_server


def sql_db() -> str:
    """Checks and returns the required SQL_DB environment variable"""
    if _sql_db is None:
        raise AttributeError("Please set SQL_DB env value")
    return _sql_db


def sql_authentication() -> str:
    """Checks and returns the sql authentication variable"""
    return _sql_authentication


def sql_user() -> str:
    """Checks and returns the required SQL_USER environment variable"""
    if _sql_user is None:
        raise AttributeError("Please set SQL_USER env value")
    return _sql_user


def sql_pass() -> str:
    """Checks and returns the required SQL_PASS environment variable"""
    if _sql_pass is None:
        raise AttributeError("Please set SQL_PASS env value")
    return _sql_pass
