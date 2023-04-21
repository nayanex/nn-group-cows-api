from cow_model.src import models as db_models
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from cow_api.src.api.v1 import models as api_models


class CowKey:
    def __init__(
        self,
        name: str = Query(
            ..., description="Name of the cow. The input will be converted to lower case."
        ),
    ):
        self.name = name


class CowParam:
    def __init__(
        self,
        cow_key: CowKey = Depends(),
    ):
        self.cow_key = cow_key

    def initialize(self, session: Session) -> None:
        self.cow = db_models.Cow.find_by_functional_key(
            self.cow_key.name, session
        ).first()

    def as_api_model(self) -> api_models.Cow:
        return api_models.Cow(
            name=self.name,
            sex= self.sex,
            birthdate=self.birthdate,
            mass_kg=self.mass_kg,
            last_measured_kg=self.last_measured_kg,
            amount_kg_feeding=self.amount_kg_feeding,
            cron_schedule_feeding=self.cron_schedule_feeding,
            last_measured_feeding=self.last_measured_feeding,
            last_milk=self.last_milk,
            cron_schedule_milk=self.cron_schedule_milk,
            amount_l=self.amount_l,
            has_calves=self.has_calves
        )

    def is_required(self) -> None:
        if self.cow is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cow does not exist")

