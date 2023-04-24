from datetime import datetime
from enum import Enum
from typing import Any


def default_audit(db_user: str, dtm: datetime = datetime.now()) -> Any:
    """Common fields to be filled when inserting a new record in an Cow table."""
    return {
        "created_by": db_user,
        "created_on": dtm,
        "modified_by": db_user,
        "modified_on": dtm,
    }


def update_audit(record: Any, db_user: str, dtm: datetime = datetime.now()) -> None:
    """Common fields to be updating when updating an existing record of an COW table."""
    record.modified_by = db_user
    record.modified_on = dtm


class CowValidationError(Exception):
    pass


class UrlValidateResultEnum(str, Enum):
    INVALID_URL = "INVALID_URL"
    OK = "OK"
