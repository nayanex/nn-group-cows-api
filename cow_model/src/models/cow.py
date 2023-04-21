import sqlalchemy as sa
from sqlalchemy.orm import Query, Session

from src.models.base import AuditBase, Base


class Cow(Base, AuditBase):
    __tablename__ = "cow"

    cow_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(250), nullable=False, unique=True)
    sex = sa.Column(sa.String(20), nullable=False)
    birthdate = sa.Column(sa.DateTime, nullable=False)
    mass_kg = sa.Column(sa.Float)
    last_measured_kg = sa.Column(sa.DateTime)
    amount_kg_feeding = sa.Column(sa.Float)
    cron_schedule_feeding = sa.Column(sa.String(15))
    last_measured_feeding = sa.Column(sa.DateTime)
    last_milk = sa.Column(sa.DateTime)
    cron_schedule_milk = sa.Column(sa.String(15))
    amount_l = sa.Column(sa.Float)
    has_calves = sa.Column(sa.Boolean, default=False)

    __table_args__ = (sa.Index("idx_cow_name", "name", unique=True), {"schema": "cow"})

    def __repr__(self) -> str:
        return f"<Cow(cow_id='{self.cow_id}', name='{self.name}')>"

    @staticmethod
    def get_all_cows(session: Session) -> Query:
        return session.query(Cow)

    @staticmethod
    def find_by_functional_key(name: str, session: Session) -> Query:
        return session.query(Cow).filter(Cow.name == name)
