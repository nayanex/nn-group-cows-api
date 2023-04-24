from typing import Any

from cow_api.src.api.v1 import cow_api
from cow_api_utils.src import app_config, create_generic_app
from fastapi import FastAPI

__version__ = "1.0.0"

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
