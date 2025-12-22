from enum import StrEnum
from typing import Any

import requests

from src.config.settings import Settings


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HttpApiManager:
    def __init__(self, base_url: str, settings: Settings) -> None:
        self.settings = settings
        self.base_url = base_url.rstrip("/")
        self.access_token = None
        self.timeout: int = 10

    def send_request(
        self,
        *,
        method: HttpMethod,
        endpoint: str,
        json: dict[str, Any] | list[dict[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        headers = {"Content-Type": "application/json"}

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        response = requests.request(
            method=method.value,
            url=f"{self.base_url}{endpoint}",
            headers=headers,
            json=json,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()
        return response.json()
