from datetime import datetime

import pytest
from fastapi.testclient import TestClient

import api.src.cow_api as cow_api
from models.src.cow import models as db_models

pytest_plugins = ["tests.conftest_db"]
LATEST_API_VERSION = 1


@pytest.fixture(scope="class")
def latest_api_vx():
    """Returns the part of version path, with the constant api version value."""
    return f"v{LATEST_API_VERSION}"


@pytest.fixture(scope="class")
def api_defaults(latest_api_vx):
    """Some default values used to use in api test methods."""

    class ApiDefaults:
        prefix_path_cow = f"/api/cow/{latest_api_vx}/cow"

    return ApiDefaults


@pytest.fixture
def user_agent():
    """Returns the name of the test agent."""
    return "Cow Test Agent"


@pytest.fixture
def default_api_int_headers_no_auth(user_agent):
    """Returns api header without authorization."""
    return {
        "Content-Type": "application/json",
        "User-Agent": user_agent,
    }


@pytest.fixture(scope="class")
def create_cow(default_audit):
    """Helper to create a data object in COW database."""

    def _cow(
        session,
        cow_id,
        name,
        sex,
        birthdate,
        condition,
        has_calves,
        mass_kg,
        last_measured_kg,
        amount_kg_feeding,
        cron_schedule_feeding,
        last_measured_feeding,
        last_milk,
        cron_schedule_milk,
        amount_l,
    ):
        cow = db_models.Cow(
            cow_id=cow_id,
            name=name,
            sex=sex,
            birthdate=birthdate,
            mass_kg=mass_kg,
            condition=condition,
            last_measured_kg=last_measured_kg,
            amount_kg_feeding=amount_kg_feeding,
            cron_schedule_feeding=cron_schedule_feeding,
            last_measured_feeding=last_measured_feeding,
            last_milk=last_milk,
            cron_schedule_milk=cron_schedule_milk,
            amount_l=amount_l,
            has_calves=has_calves,
            **default_audit,
        )
        session.add(cow)
        session.flush()
        return cow

    return _cow


@pytest.fixture(scope="class")
def default_audit():
    """Used to fill in the default attributes in most tables of the COW db."""
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    return {
        "created_by": "CowAuditor",
        "created_on": today,
        "modified_by": "CowAuditor",
        "modified_on": today,
    }


@pytest.fixture(scope="session")
def api_test_client():
    """Helper to create and returns a request in the COW api."""
    app = cow_api.create_app()
    client = TestClient(app)
    return client
