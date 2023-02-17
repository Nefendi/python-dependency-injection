from dependency_injector import containers, providers

from .services import ManagementFacade, UserService, WebClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yaml"])

    # This is not needed, we can set it later using container.wire().
    # If this is defined, the container automatically calls .wire() method upon instantiation.
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    web_client = providers.Factory(
        WebClient, address=config.web_client.address, port=config.web_client.port
    )

    user_service = providers.Factory(
        UserService,
        web_client=web_client,
        verbosity_level=config.user_service.verbosity_level,
    )

    management_facade = providers.Factory(ManagementFacade, user_service=user_service)
