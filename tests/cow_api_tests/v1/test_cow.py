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
            cow_id=1,
            sex="female",
            birthdate=datetime.now().replace(second=0, microsecond=0),
            condition="Healthy",
            has_calves=False,
            mass_kg=90,
            last_measured_kg=datetime.now().replace(second=0, microsecond=0),
            name="cow1",
            session=session,
            amount_kg_feeding=20,
            cron_schedule_feeding="0 8,12,16,20 * * *",
            last_measured_feeding=datetime.now().replace(second=0, microsecond=0),
            last_milk=datetime.now().replace(second=0, microsecond=0),
            cron_schedule_milk="0 8,12,16,20 * * *",
            amount_l=2,
        )
    response = api_test_client.get(url=api_defaults.prefix_path_cow + "/cows", headers=default_api_int_headers_no_auth)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response[0]["name"] == "cow1"

    with session_scope() as session2:
        create_cow(
            cow_id=2,
            sex="male",
            birthdate=datetime.now().replace(second=0, microsecond=0),
            condition="Healthy",
            has_calves=True,
            mass_kg=90,
            last_measured_kg=datetime.now().replace(second=0, microsecond=0),
            name="cow2",
            session=session2,
            amount_kg_feeding=20,
            cron_schedule_feeding="0 8,12,16,20 * * *",
            last_measured_feeding=datetime.now().replace(second=0, microsecond=0),
            last_milk=datetime.now().replace(second=0, microsecond=0),
            cron_schedule_milk="0 8,12,16,20 * * *",
            amount_l=5,
        )

    response = api_test_client.get(url=api_defaults.prefix_path_cow + "/cows", headers=default_api_int_headers_no_auth)
    assert response.status_code == 200
    assert "cow1" == response.json()[0]["name"]
    assert "cow2" == response.json()[1]["name"]
