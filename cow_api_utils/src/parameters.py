"""parameters.py - Set the Session and Common parameters."""
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker


@contextmanager
def session_scope() -> Session:
    """Returns a contextmanager used to connect and manage a session to the database."""
    _session = sessionmaker(autocommit=False, autoflush=False, bind=engine())()
    try:
        yield _session
    finally:
        _session.close()
