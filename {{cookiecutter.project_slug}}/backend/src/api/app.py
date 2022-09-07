import http
import logging
from json import JSONDecodeError

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from requests import HTTPError
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.v1 import views as v1_views
from api.utils import ErrorModel
from api.basic import views as basic_views
from config.base import app_settings as settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.NAME, version=settings.VERSION)
    _setup_routes(app)
    _setup_exception_handling(app)
    _setup_middlewares(app)

    return app


def _setup_routes(app: FastAPI) -> None:
    app.include_router(
        v1_views.router,
        prefix=f"{settings.BASE_PATH}/v1",
        responses={
            http.HTTPStatus.BAD_REQUEST.value: {"model": ErrorModel},
            http.HTTPStatus.UNPROCESSABLE_ENTITY.value: {"model": ErrorModel},
            http.HTTPStatus.INTERNAL_SERVER_ERROR.value: {"model": ErrorModel},
            http.HTTPStatus.CONFLICT.value: {"model": ErrorModel},
        },
    )
    app.include_router(
        basic_views.router,
        prefix=settings.BASE_PATH,
        tags=["basic"],
        responses={
            # fmt: off
            http.HTTPStatus.UNPROCESSABLE_ENTITY.value: {"model": ErrorModel}
            # fmt: on
        },
    )


def _setup_exception_handling(app: FastAPI) -> None:
    app.exception_handler(HTTPError)(http_handler)
    app.exception_handler(ValidationError)(pydantic_error_handler)
    app.exception_handler(Exception)(handler)


async def pydantic_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    logging.getLogger("App").error(f"caught validation error {exc.args}")
    return JSONResponse(
        status_code=500,
        content=ErrorModel(message=str(exc.args), key=None, code=500).dict(),
    )


async def http_handler(request: Request, exc: HTTPError) -> JSONResponse:
    try:
        content = (await exc.response.json(),)
    except JSONDecodeError:  # pragma: nocover
        content = exc.response.reason
    except TypeError:
        content = (exc.response.json(),)

    return JSONResponse(
        status_code=exc.response.status_code,
        content=content,
    )


async def handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=ErrorModel(message=str(exc), key=None, code=500).dict(),
    )


def _setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
    )


application = create_app()
