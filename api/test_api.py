from dataclasses import dataclass
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from .application import app
from .endpoints import web_client_factory
from .services import WebClient


@dataclass
class WebClientTestDouble(WebClient):
    address: str = "https://test.address.com"
    port: str = "8000"

    def make_a_request(self) -> None:
        print("I'm only a test implementation of the make_a_request function :(")


def web_client_test_double_factory() -> WebClient:
    return WebClientTestDouble()


@pytest.fixture()
def client():
    with TestClient(app=app) as client:
        yield client


# First way - no dependency injection at all
def test_register_a_user_using_no_dependency_injection(client):
    with patch.object(
        WebClient,
        "make_a_request",
        spec_set=WebClient,
        side_effect=lambda: print(
            "I'm only a test implementation of the make_a_request function :("
        ),
    ):
        response = client.post("/no-dependency-injection")

    assert response.status_code == 200


# Second way - using dependency injection built into FastAPI
def test_register_a_user_using_fastapi_dependency_injection(client):
    # Override the dependency using FastAPI's built-in mechanisms
    app.dependency_overrides[web_client_factory] = web_client_test_double_factory

    response = client.post("/fastapi-dependency-injection")

    # A necessary clean-up
    app.dependency_overrides = {}

    assert response.status_code == 200
    assert response.json() == {
        "address": "https://test.address.com",
        "port": "8000",
    }


# Third way - using the dependency-injector package
def test_register_a_user_using_dependency_injector(client):
    web_client_test_double = WebClientTestDouble()

    # Override the dependency using dependency-injector's capabilities
    with app.container.web_client.override(web_client_test_double):
        response = client.post("/dependency-injector")

    assert response.status_code == 200
    assert response.json() == {
        "address": "https://test.address.com",
        "port": "8000",
    }
