from datetime import datetime

from dotenv import load_dotenv

load_dotenv("test.env", override=True)


def test_empty(api_test_client, api_defaults, default_api_int_headers_no_auth, clear_database):
    response = api_test_client.get(url=api_defaults.prefix_path_cow + "/cows", headers=default_api_int_headers_no_auth)
    assert response.status_code == 200
    assert response.json() == []


def test_get_cows(
    session_scope,
    api_test_client,
    api_defaults,
    default_api_int_headers_no_auth,
    create_cow,
    clear_database,
):
    with session_scope() as session:
        create_cow(
            sex="female",
            birthdate=datetime.now(),
            condition="Healthy",
            has_calves=False,
            mass_kg=90,
            last_measured_kg=datetime.now(),
            name="cow1",
            session=session,
            amount_kg_feeding=20,
            cron_schedule_feeding="0 8,12,16,20 * * *",
            last_measured_feeding=datetime.now(),
            last_milk=datetime.now(),
            cron_schedule_milk="0 8,12,16,20 * * *",
            amount_l=2,
        )
    response = api_test_client.get(
        url=api_defaults.prefix_path_data_object + "/cows", headers=default_api_int_headers_no_auth
    )
    assert response.status_code == 200
    assert response.json() == ["cow1"]

    with session_scope() as session2:
        create_cow(
            sex="male",
            birthdate=datetime.now(),
            condition="Healthy",
            has_calves=True,
            mass_kg=90,
            last_measured_kg=datetime.now(),
            name="cow2",
            session=session2,
            amount_kg_feeding=20,
            cron_schedule_feeding="0 8,12,16,20 * * *",
            last_measured_feeding=datetime.now(),
            last_milk=datetime.now(),
            cron_schedule_milk="0 8,12,16,20 * * *",
            amount_l=5,
        )

    response = api_test_client.get(url=api_defaults.prefix_path_cow + "/cows", headers=default_api_int_headers_no_auth)
    assert response.status_code == 200
    assert response.json() == ["cow1", "cow2"]
