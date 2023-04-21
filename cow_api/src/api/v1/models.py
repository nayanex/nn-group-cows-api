from datetime import datetime
from typing import Optional

from cow_model.src import models as db_models
from cow_api_utils.src.models import BaseModel


class Feeding(BaseModel):
    amount_kg: Optional[float] = None
    cron_schedule: Optional[str] = None
    last_measured: Optional[datetime] = None


class Weight(BaseModel):
    mass_kg: Optional[float] = None
    last_measured: Optional[datetime] = None


class MilkProduction(BaseModel):
    last_milk: Optional[datetime] = None
    cron_schedule: Optional[str] = None
    amount_l: Optional[float] = None

class Cow(BaseModel):
    name: Optional[str] = None
    sex: Optional[str] = None
    birthdate: Optional[datetime] = None
    condition: Optional[str] = None
    weight: Optional[Weight] = None
    feeding: Optional[Feeding] = None
    milk_production: Optional[MilkProduction] = None
    has_calves: Optional[bool] = False

    @classmethod
    def from_db_model(cls, cow: db_models.Cow) -> "Cow":
        weight = Weight(
            mass_kg = cow.mass_kg,
            last_measured = cow.last_measured_kg
        )

        feeding = Feeding(
            amount_kg = cow.amount_kg_feeding,
            cron_schedule = cow.cron_schedule_feeding,
            last_measured = cow.last_measured_feeding
        )

        milk_production = MilkProduction(
            last_milk = cow.last_milk,
            cron_schedule = cow.cron_schedule_milk,
            amount_l = cow.amount_l
        )

        return Cow(
            name=cow.name,
            sex=cow.sex.data_producer.name,
            birthdate=cow.birthdate.name,
            condition=cow.condition,
            weight=weight,
            feeding=feeding,
            milk_production=milk_production,
            has_calves=cow.has_calves,
        )




