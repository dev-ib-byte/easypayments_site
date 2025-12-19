from enum import StrEnum
from typing import Any

import requests

from src.infrastructure.managers.base import ApiManager


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HttpApiManager:
    def __init__(self, base_url: str, access_token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
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
