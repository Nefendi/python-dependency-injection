from fastapi import FastAPI

from . import endpoints
from .container import Container


def create_app() -> FastAPI:
    container = Container()

    application = FastAPI()
    application.container = container
    application.include_router(endpoints.router)

    return application


app = create_app()
