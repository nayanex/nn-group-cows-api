"""db.py - provide methods related to the database interface."""
import logging
import os
import struct
from contextlib import contextmanager
from typing import Any, Dict
from urllib import parse as urllib_parse

import sqlalchemy as sa
from azure import identity
from azure.core.credentials import AccessToken
from azure.core.exceptions import ClientAuthenticationError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from emr_api_utils import app_config

sqlite_schemas = {}

SQLITE_PATH_EMR = os.getenv("SQLITE_PATH_EMR")
SQL_COPT_SS_ACCESS_TOKEN = 1256
DATABASE_ACCESS_TOKEN_URL = "https://database.windows.net/"  # nosec


def retrieve_database_token(credential: Any, token_url: str = DATABASE_ACCESS_TOKEN_URL) -> bytes:
    """Retrieves a token and converts it so it can be used in pyodbc/SqlAlchemy to connect to a database
    using a System or User Assigned Managed Identity.
        Args:
            credential: ManagedIdentityCredential instance (azure.identity)
            token_url: Pre-defined token url using Azure Sql Server constant.
        Returns:
            bytes: Bytes object with token encoded
    """
    # Use azure.identity credential to get a token
    access_token: AccessToken = credential.get_token(token_url)
    logging.debug(f"Database access token retrieved: {access_token}")

    # Encode token in such a way that pyodbc understands it
    token_string = bytes(access_token.token, "utf-8")
    exp_token = b""
    for i in token_string:
        exp_token += bytes({i})
        exp_token += bytes(1)
    token_struct = struct.pack("=i", len(exp_token)) + exp_token

    return token_struct


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
    if protocol == "msimssql":
        try:
            umi_client_id = app_config.umi_client_id()
            if umi_client_id is not None and len(umi_client_id.rstrip()) > 0:
                logging.info("Connecting to database using user-assigned managed id")
                credential = identity.ManagedIdentityCredential(client_id=umi_client_id)
            else:
                logging.info("Connecting to database using system managed id")
                credential = identity.DefaultAzureCredential(exclude_shared_token_cache_credential=True)
        except ClientAuthenticationError as ca_error:
            logging.exception(
                "Authentication error while connecting to the database",
                exc_info=ca_error,
            )
            raise ca_error
        except Exception as e:
            logging.exception(e)
            raise e

        token_struct = retrieve_database_token(credential=credential)
        connect_args["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}

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
