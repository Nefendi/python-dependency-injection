from dataclasses import dataclass


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


def main(mgmt: ManagementFacade) -> None:
    mgmt.register_user()


if __name__ == "__main__":
    mgmt = ManagementFacade(
        user_service=UserService(
            verbosity_level="CONCISE",
            web_client=WebClient(address="https://xyz.com", port="7000"),
        )
    )

    main(mgmt)
