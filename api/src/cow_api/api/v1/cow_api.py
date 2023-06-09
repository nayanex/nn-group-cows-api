from datetime import datetime
from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.params import Body, Query

from api.src.cow_api.api.v1 import models as api_models
from api.src.cow_api.utils.parameters import CowParam
from models.src.cow import models as db_models
from utils.src.cow_api_utils.parameters import session_scope

router = APIRouter()

base_path = "/cow"


@router.get(
    base_path + "/cows",
    response_model=List[api_models.Cow],
)
async def get_cows() -> List[api_models.Cow]:

    with session_scope() as session:
        cows = session.query(db_models.Cow).all()
        return [api_models.Cow.from_db_model(c) for c in cows]


@router.post(
    base_path,
    status_code=201,
    response_model=api_models.Cow,
    responses={400: {"description": "Bad request: Already exists"}, 404: {"description": "Bad request: Not found"}},
)
async def create_cow(
    request: Request,
    cw: CowParam = Depends(),
    body: api_models.Cow = Body(..., description="The body input"),
    overwrite: bool = Query(False, description="Decides whether record should be updated or not"),
) -> api_models.Cow:
    """<p>Checks whether cow that is provided in the body exists in the database.<br>
    Creates cow if it does not exist.</p>
    <p>Setting the overwrite parameter to true will create the cow if it does not exist or will update the cow with the
    input in the body if it does exist.<br>
    When updating a record, the modification date and modified by will be modified as well.</p>"""
    now = datetime.now()
    json = await request.json()
    with session_scope() as session:
        cw.initialize(session=session)

        if not overwrite and cw.name is not None:
            raise HTTPException(status_code=400, detail="Cow already exist")
        if cw.name is None:
            cw.name = db_models.Cow(
                name=cw.cow_key.name,
                created_by="API System",
                created_on=now,
                sex=body.sex,
                birthdate=body.birthdate,
                mass_kg=body.mass_kg,
                last_measured_kg=body.last_measured_kg,
                amount_kg_feeding=body.amount_kg_feeding,
                cron_schedule_feeding=body.cron_schedule_feeding,
                last_measured_feeding=body.last_measured_feeding,
                last_milk=body.last_milk,
                cron_schedule_milk=body.cron_schedule_milk,
                amount_l=body.amount_l,
                has_calves=body.has_calves,
            )
            session.add(cw.cow)
        else:
            update_fields_cow(json, body, cw.cow)
        cw.cow.modified_by = cw.object_id
        cw.cow.modified_on = now
        session.commit()

        return cw.as_api_model()


def update_fields_cow(json: Any, body: Any, cow: db_models.Cow) -> None:
    if "birthdate" in json:
        cow.birthdate = body.birthdate
    if "mass_kg" in json:
        cow.mass_kg = body.mass_kg
    if "last_measured_kg" in json:
        cow.last_measured_kg = body.last_measured_kg
    if "amount_kg_feeding" in json:
        cow.amount_kg_feeding = body.amount_kg_feeding
    if "cron_schedule_feeding" in json:
        cow.cron_schedule_feeding = body.cron_schedule_feeding
    if "last_milk" in json:
        cow.last_milk = body.last_milk
    if "amount_l" in json:
        cow.amount_l = body.amount_l
    if "has_calves" in json:
        cow.has_calves = body.has_calves


@router.get(base_path, response_model=api_models.Cow, responses={404: {"description": "Bad request: Not found"}})
async def get_cow(
    cw: CowParam = Depends(),
) -> api_models.Cow:
    """Returns the data producer that is provided as input."""
    with session_scope() as session:
        cw.initialize(session=session)
        cw.is_required()

        return cw.as_api_model()


@router.delete(
    base_path,
    status_code=HTTPStatus.NO_CONTENT,
    response_class=Response,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Bad request: Not found"}},
)
async def delete(
    cw: CowParam = Depends(CowParam),
) -> Response:
    """Deletes the data producer that is provided as input."""
    with session_scope() as session:
        cw.initialize(session=session)
        cw.is_required()

        session.delete(cw.cow)
        session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    base_path,
    status_code=201,
    response_model=api_models.Cow,
    responses={404: {"description": "Bad request: Not found"}},
)
async def put(
    request: Request,
    cw: CowParam = Depends(),
    body: api_models.Cow = Body(..., description="The body input"),
) -> api_models.Cow:
    """Updates the cow record with the body input.<br>
    The modification date and modified by columns will also be modified."""
    with session_scope() as session:
        cw.initialize(session=session)
        cw.is_required()

        now = datetime.now()
        json = await request.json()
        if "name" in json:
            cw.cow.name = body.name
        update_fields_cow(json, body, cw.cow)
        cw.cow.modified_by = "API System"
        cw.cow.modified_on = now
        session.commit()

        return cw.as_api_model()
