import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SQL_PROTOCOL = os.environ.get("SQL_PROTOCOL") or "secret-key"

    SQL_SERVER = os.environ.get("SQL_SERVER") or "0.0.0.0"
    SQL_DB = os.environ.get("SQL_DB") or "ENTER_SQL_DB_NAME"
    SQL_USER = os.environ.get("SQL_USER") or "ENTER_SQL_SERVER_USERNAME"
    SQL_PASS = os.environ.get("SQL_PASS") or "ENTER_SQL_SERVER_PASSWORD"
    SQL_AUTHENTICATION = os.environ.get("SQL_AUTHENTICATION") or "ENTER_SQL_AUTHENTICATION"
    ODBC_DRIVER = os.environ.get("ODBC_DRIVER") or "ENTER_SQL_ODBC_DRIVER"
