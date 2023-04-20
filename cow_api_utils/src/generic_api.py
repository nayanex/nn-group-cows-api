"""generic_api.py - Methods related to router generation."""
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from cow_api_utils.src import app_config
from cow_api_utils.src.parameters import session_scope


def create_generic_router(module_versions: Optional[dict] = None) -> APIRouter:
    """Create and configure the routes used by api.
    Args:
        module_versions: List of module version returned by the versions endpoint
    Returns:
        APIRouter: API statuses
    """
    router = APIRouter()

    @router.get("/status")
    def status() -> str:
        """Provide an endpoint to check if the service is running"""
        return "API up"

    @router.get("/db_check")
    def db_check() -> str:
        """Provide an endpoint to check if the database is running and connected"""
        with session_scope() as sp:
            # Result here is not important, query not raise an error
            statement = text("SELECT 1")
            try:
                sp.execute(statement).fetchall()
                return "OK"
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"DB Connection Error:{e}")

    @router.get("/version")
    def version() -> Dict[str, Any]:
        """Provide an endpoint to list the api version details"""
        return {
            "build_id": app_config.build_id(),
            "commit_id": app_config.commit_id(),
            "modules": module_versions,
        }
