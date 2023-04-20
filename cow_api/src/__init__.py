from typing import Any

import cow_model
import cow_api_utils
import pkg_resources
from cow_api_utils import app_config, create_generic_app
from fastapi import FastAPI

from cow_api.api.v1 import (
    cow_api,
    feeding_api,
    milk_production_api
)
from cow_api.utils.mask_headers import mask_headers  # noqa: F401

__version__ = pkg_resources.get_distribution("cow_api").version

cow_api_app = None


def module_versions() -> Any:
    return {
        "cow_api": __version__,
        "cow_model": cow_model.__version__,
        "cow_api_utils": cow_api_utils.__version__,
    }


def create_cow_app_v1() -> FastAPI:
    app_v1 = create_generic_app(
        title="COW API",
        version=__version__,
        module_versions=module_versions(),
    )
    app_v1.root_path = "/api/cow/v1"
    app_v1.include_router(cow_api.router, tags=["Data Producer"])
    app_v1.include_router(feeding_api.router, tags=["Data Set"])
    app_v1.include_router(milk_production_api.router, tags=["Storage Account"])

    return app_v1

def create_app() -> FastAPI:
    global cow_api_app

    app_config.api_group = "cow"
    app = create_generic_app("COW API", __version__, module_versions=module_versions())

    cow_api_app = create_cow_app_v1()
    app.mount("/api/cow/v1", cow_api_app)

    return app
