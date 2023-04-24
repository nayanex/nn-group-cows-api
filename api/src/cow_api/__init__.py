from typing import Any

from fastapi import FastAPI

from api.src.cow_api.api.v1 import cow_api
from utils.src.cow_api_utils import app_config, create_generic_app

__version__ = 1

cow_api_app = None


def module_versions() -> Any:
    return {
        "cow_api": __version__,
        # "cow_model": cow_model.__version__,
        # "cow_api_utils": cow_api_utils.__version__,
    }


def create_cow_app_v1() -> FastAPI:
    app_v1 = create_generic_app(
        title="COW API",
        version=__version__,
        module_versions=module_versions(),
    )
    app_v1.root_path = "/api/cow/v1"
    app_v1.include_router(cow_api.router, tags=["Cow"])

    return app_v1


def create_app() -> FastAPI:
    global cow_api_app

    app_config.api_group = "cow"
    app = create_generic_app("COW API", __version__, module_versions=module_versions())

    cow_api_app = create_cow_app_v1()
    app.mount("/api/cow/v1", cow_api_app)

    return app
