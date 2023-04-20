import logging
import os
from typing import Any

import uvicorn
from starlette.requests import Request

from emr_api import create_app, mask_headers

logging.basicConfig(level=os.getenv("LOG_LEVEL", default="INFO"))

if __name__ == "__main__":
    app = create_app()

    @app.middleware("http")
    async def log_requests_responses(request: Request, call_next: Any) -> Any:
        try:
            logging.info(f"request headers: {mask_headers(request)}")
        except (KeyError, AttributeError) as e:
            logging.exception(e)
            raise e

        try:
            logging.info(f"request: {request.json()}")
        except Exception as e:
            logging.exception(e)

        response = await call_next(request)

        try:
            logging.info(f"response headers: {mask_headers(response)}")
        except (KeyError, AttributeError) as e:
            logging.exception(e)
            raise e

        return response

    port_string = os.getenv("PORT")
    if port_string is not None:
        port = int(port_string)
    else:
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True)
