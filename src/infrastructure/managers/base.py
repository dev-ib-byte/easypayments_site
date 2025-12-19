from abc import ABC

class ApiManager(ABC):
    def __init__(self, base_url: str, access_token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
        self.timeout: int = 10
