from datetime import datetime
from typing import Any, Dict, List

from cow_model import models as db_models
from cow_api_utils.parameters import session_scope
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.params import Body, Query

from emr_api.api.v1 import models as api_models
from emr_api.utils.parameters import CowParam, FeedingParam, MilkProductionParam

router = APIRouter()

base_path = "/cow"

@router.get(
    base_path + "/cows",
    response_model=List[api_models.DeliveryRetention],
)
async def get_cows(
) -> List[api_models.Cows]:

    with session_scope() as session:
        cows = session.query(db_models.Cow)
        return [api_models.Cow.from_db_model(c) for c in cows]