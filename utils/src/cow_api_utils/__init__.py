from typing import Optional

import pkg_resources  # type: ignore
from fastapi import FastAPI, Response
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from models.src.cow import CowValidationError

from . import app_config
from .generic_api import create_generic_router

__version__ = pkg_resources.get_distribution("cow_api_utils").version


class RedirectException(Exception):
    """Raised by FastAPI when a redirect occurs"""

    def __init__(self, url: str, cookies: Optional[dict] = None):
        self.url = url
        self.cookies = cookies or {}


def create_generic_app(
    title: str,
    version: str,
    openapi_prefix: Optional[str] = None,
    module_versions: Optional[dict] = None,
) -> FastAPI:
    """Create and return the FastAPI app instance"""
    app = FastAPI(
        title=title,
        version=version,
        debug=app_config.debug(),
        openapi_prefix=openapi_prefix,
    )

    @app.exception_handler(RedirectException)
    async def handle_redirect_exception(request: Request, exc: RedirectException) -> Response:
        """Custom exception handler to RedirectException setting the cookies"""
        response = RedirectResponse(url=exc.url)
        for k, v in exc.cookies.items():
            response.set_cookie(k, v)
        return response

    @app.exception_handler(CowValidationError)
    async def handle_emr_validation_error(request: Request, exc: CowValidationError) -> Response:
        """Override the default exception handler.
        Args:
            request[Request]: Http request handler
            exc[CowValidationError]: Exception from cow.utils package.
        Returns:
            Response: Http Response handler in a JSON format.
        """
        return JSONResponse({"name": "CowValidationError", "detail": str(exc)}, status_code=422)

    app.include_router(create_generic_router(module_versions=module_versions), tags=["Generic"])

    return app
