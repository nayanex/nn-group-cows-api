from datetime import datetime
from typing import Optional

from models.src.cow import models as db_models
from utils.src.cow_api_utils.models import BaseModel


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
        weight = Weight(mass_kg=cow.mass_kg, last_measured=cow.last_measured_kg)

        feeding = Feeding(
            amount_kg=cow.amount_kg_feeding,
            cron_schedule=cow.cron_schedule_feeding,
            last_measured=cow.last_measured_feeding,
        )

        milk_production = MilkProduction(
            last_milk=cow.last_milk, cron_schedule=cow.cron_schedule_milk, amount_l=cow.amount_l
        )

        return Cow(
            name=cow.name,
            sex=cow.sex,
            birthdate=cow.birthdate,
            condition=cow.condition,
            weight=weight,
            feeding=feeding,
            milk_production=milk_production,
            has_calves=cow.has_calves,
        )
