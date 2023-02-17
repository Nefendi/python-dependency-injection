from dataclasses import dataclass
from unittest.mock import MagicMock

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


@dataclass
class WebClient:
    address: str
    port: str

    def make_a_request(self) -> None:
        print(f"Making a request to {self.address}:{self.port}")


@dataclass
class UserService:
    verbosity_level: str
    web_client: WebClient

    def register(self) -> None:
        print(
            f"Registering a user with verbosity level set to {self.verbosity_level}..."
        )

        self.web_client.make_a_request()


@dataclass
class ManagementFacade:
    user_service: UserService

    def register_user(self) -> None:
        print("Registering a user...")

        self.user_service.register()

        print("Done!")


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])

    # This is not needed, we can set it later using container.wire().
    # If this is defined, the container automatically calls .wire() method upon instantiation.
    wiring_config = containers.WiringConfiguration(modules=[__name__])

    web_client = providers.Factory(
        WebClient, address=config.web_client.address, port=config.web_client.port
    )

    user_service = providers.Factory(
        UserService,
        web_client=web_client,
        verbosity_level=config.user_service.verbosity_level,
    )

    management_facade = providers.Factory(ManagementFacade, user_service=user_service)


@inject
def main(mgmt: ManagementFacade = Provide[Container.management_facade]) -> None:
    mgmt.register_user()


if __name__ == "__main__":
    container = Container()
    # container.wire(modules=[__name__])

    main()

    # Overriding for testing purposes
    # web_client_mock = MagicMock(
    #     spec_set=WebClient(address="", port=""),
    #     make_a_request=MagicMock(
    #         side_effect=lambda: print(
    #             "I'm only a test implementation of the make_a_request function :("
    #         )
    #     ),
    # )

    # with container.web_client.override(web_client_mock):
    #     main()
