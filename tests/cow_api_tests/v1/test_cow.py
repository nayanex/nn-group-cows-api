from datetime import datetime

import pytest

from emr.models import Cow, MilkProduction, Feeding


def test_empty(
    api_test_client, api_defaults, default_api_int_headers_no_auth, clear_database
):
    response = api_test_client.get(
        url=api_defaults.prefix_path_cow + "/list", headers=default_api_int_headers_no_auth
    )
    assert response.status_code == 200
    assert response.json() == []


def test_get_cows(
    session_scope,
    api_test_client,
    api_defaults,
    default_api_int_headers_no_auth,
    create_cow,
    clear_database,
    create_feeding,
    create_milk_production
):
    with session_scope() as session:
        fe = session.query(db_models.Feeding).one()
        mp = session.query(db_models.MilkProduction).one()
        create_cow(
            sex="female",
            birthdate=datetime.now(),
            condition="Healthy",
            has_calves=True,
            mass_kg=120,
            last_measured=datetime.now(),
            feeding_id=fe.feeding_id,
            milk_production_id=mp.milk_production_id,
            name="cow1",
            session=session,
        )
    response = api_test_client.get(
        url=api_defaults.prefix_path_data_object + "/cows", headers=default_api_int_headers_no_auth
    )
    assert response.status_code == 200
    assert response.json() == ["cow1"]

    with session_scope() as session2:
        fe = session.query(db_models.FileSystem).one()
        mp = session.query(db_models.DataProducer).one()
        create_cow(
            sex="male",
            birthdate=datetime.now(),
            condition="Healthy",
            has_calves=True,
            mass_kg=90,
            last_measured=datetime.now(),
            feeding_id=fe.feeding_id,
            milk_production_id=mp.milk_production_id,
            name="cow2",
            session=session,
        )

    response = api_test_client.get(
        url=api_defaults.prefix_path_cow + "/list", headers=default_api_int_headers_no_auth
    )
    assert response.status_code == 200
    assert response.json() == ["cow1", "cow2"]

