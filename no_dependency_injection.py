class WebClient:
    def __init__(self) -> None:
        self.address = "https://xyz.com"
        self.port = "7000"

    def make_a_request(self) -> None:
        print(f"Making a request to {self.address}:{self.port}")


class UserService:
    def __init__(self) -> None:
        self.web_client = WebClient()
        self.verbosity_level = "CONCISE"

    def register(self) -> None:
        print(
            f"Registering a user with verbosity level set to {self.verbosity_level}..."
        )

        self.web_client.make_a_request()


class ManagementFacade:
    def __init__(self) -> None:
        self.user_service = UserService()

    def register_user(self) -> None:
        print("Registering a user...")

        self.user_service.register()

        print("Done!")


def main() -> None:
    mgmt = ManagementFacade()

    mgmt.register_user()


if __name__ == "__main__":
    main()
