from datetime import datetime

import pytest
from cow_model import models as db_models
from fastapi.testclient import TestClient

import cow_api

pytest_plugins = ["tests.conftest_db", "tests.conftest_int"]
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
        prefix_path_milk_production = f"/api/cow/{latest_api_vx}/milk_production"
        prefix_path_feeding = f"/api/cow/{latest_api_vx}/feeding"

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


@pytest.fixture
def create_milk_production(default_audit):
    """Helper to create a dataset in COW database."""

    def _milk_production(session, last_milk, cron_schedule, amount_l):
        mp = db_models.MilkProduction(
            last_milk=last_milk,
            cron_schedule=cron_schedule,
            amount_l=amount_l,
            **default_audit,
        )
        session.add(mp)
        session.flush()
        return mp

    return _milk_production


@pytest.fixture(scope="class")
def create_cow(default_audit):
    """Helper to create a data object in COW database."""

    def _cow(
        session,
        name,
        sex,
        birthdate,
        condition,
        has_calves,
        mass_kg,
        last_measured,
        feeding_id,
        milk_production_id,
    ):
        cow = db_models.Cow(
            name=name,
            sex=sex,
            birthdate=birthdate,
            condition=condition,
            has_calves=has_calves,
            mass_kg=mass_kg,
            last_measured=last_measured,
            feeding_id=feeding_id,
            milk_production_id=milk_production_id,
            **default_audit
        )
        session.add(cow)
        session.flush()
        return cow

    return _cow


@pytest.fixture(scope="class")
def create_feeding(default_audit):
    """Helper to create a feeding in the COW database."""

    def _feeding(
        session, amount_kg, cron_schedule, last_measured
    ):
        fe = db_models.Feeding(
            amount_kg=amount_kg,
            cron_schedule=cron_schedule,
            last_measured=last_measured
            **default_audit,
        )
        session.add(fe)
        session.flush()
        return fe

    return _feeding


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


