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
    weight: Optional[Weight] = None
    feeding: Optional[Feeding] = None
    milk_production: Optional[MilkProduction] = None
    has_calves: Optional[bool] = False




