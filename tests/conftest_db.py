from contextlib import contextmanager

import pytest
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.schema import CreateSchema, DropSchema

from models.src.cow import models
from models.src.cow.connection import clean_database
from utils.src.cow_api_utils import app_config
from utils.src.cow_api_utils.db import create_session
from utils.src.cow_api_utils.db import engine as eau_engine

ENGINE_SCHEMA = "cow"
SessionLocal = None


@pytest.fixture(scope="session")
def engine():
    """Helper to create the engine to COW database. Supports sqlite and Mssql."""
    return eau_engine()


@pytest.fixture(scope="session")
def session_scope(engine):
    """Provide a transactional scope around a series of operations."""

    @contextmanager
    def _create_session() -> Session:
        """Creates a database session using given configuration."""
        global SessionLocal

        if not SessionLocal:
            sm = sessionmaker(bind=engine())
            SessionLocal = scoped_session(sm)
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    return create_session


@pytest.fixture(scope="session")
def create_schema(engine, session_scope):
    """Helper to create a schema in COW database. Supports sqlite and mssql."""
    if app_config.sql_protocol() == "mssql":
        if ENGINE_SCHEMA in engine.dialect.get_schema_names(engine):
            with session_scope() as session:
                clean_database(session=session)
            engine.execute(DropSchema(name=ENGINE_SCHEMA))
        engine.execute(CreateSchema(ENGINE_SCHEMA))


@pytest.fixture(scope="class")
def create_cow_tables(engine, create_schema):
    """Create all tables in COW database."""
    models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="class")
def clear_database(create_cow_tables, session_scope):
    """Helper to clean the COW data tables."""
    with session_scope() as session:
        session.query(models.Cow).delete()
        session.commit()
