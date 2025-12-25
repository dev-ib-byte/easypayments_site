import ssl
from enum import StrEnum
from typing import Any, Mapping

import aiohttp
import certifi

from src.config.settings import Settings

JsonType = dict[str, Any] | list[dict[str, Any]]


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
        self.access_token: str | None = None
        self.timeout: int = 10
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            ssl_ctx = ssl.create_default_context(cafile=certifi.where())
            timeout = aiohttp.ClientTimeout(total=self.timeout)

            self._session = aiohttp.ClientSession(
                timeout=timeout,
                connector=aiohttp.TCPConnector(ssl=ssl_ctx, limit=100),
                raise_for_status=False,
            )
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    async def send_request(
        self,
        *,
        method: HttpMethod,
        endpoint: str,
        json: JsonType | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"

        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        async with session.request(  # type: ignore
            method=method.value,
            url=url,
            params=params,
            json=json,
            headers=headers,
        ) as response:

            data = await response.text()

            if response.status >= 400:
                raise RuntimeError(f"HTTP {response.status} {url}: {data}")

            if "application/json" in response.headers.get("Content-Type", ""):
                return await response.json()

            return data
