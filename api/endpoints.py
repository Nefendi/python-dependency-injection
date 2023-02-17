from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .container import Container
from .services import ManagementFacade, UserService, WebClient


class Response(BaseModel):
    address: str
    port: str


router = APIRouter()


# First way - no dependency injection at all
@router.post("/no-dependency-injection", response_model=Response)
def register_a_user_with_no_dependency_injection():
    mgmt_facade = ManagementFacade(
        user_service=UserService(
            verbosity_level="CONCISE",
            web_client=WebClient(address="https://xyz.com", port="7000"),
        )
    )

    mgmt_facade.register_user()

    return {
        "address": mgmt_facade.user_service.web_client.address,
        "port": mgmt_facade.user_service.web_client.port,
    }


def web_client_factory() -> WebClient:
    return WebClient(address="https://xyz.com", port="7000")


def user_service_factory(
    web_client: WebClient = Depends(web_client_factory),
) -> UserService:
    return UserService(
        verbosity_level="CONCISE",
        web_client=web_client,
    )


def mgmt_facade_factory(
    user_service: UserService = Depends(user_service_factory),
) -> ManagementFacade:
    return ManagementFacade(user_service=user_service)


# Second way - using dependency injection built into FastAPI
@router.post("/fastapi-dependency-injection", response_model=Response)
def register_a_user_using_fastapi_dependency_injection(
    mgmt_facade: ManagementFacade = Depends(mgmt_facade_factory),
):
    mgmt_facade.register_user()

    return {
        "address": mgmt_facade.user_service.web_client.address,
        "port": mgmt_facade.user_service.web_client.port,
    }


# Third way - using the dependency-injector package
@router.post("/dependency-injector", response_model=Response)
@inject
def register_a_user_using_dependency_injector(
    mgmt_facade: ManagementFacade = Depends(Provide[Container.management_facade]),
):
    mgmt_facade.register_user()

    return {
        "address": mgmt_facade.user_service.web_client.address,
        "port": mgmt_facade.user_service.web_client.port,
    }
