import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuditBase:
    created_on = sa.Column(sa.DateTime, nullable=False)
    created_by = sa.Column(sa.String(50), nullable=False)
    modified_on = sa.Column(sa.DateTime, nullable=False)
    modified_by = sa.Column(sa.String(50), nullable=False)
