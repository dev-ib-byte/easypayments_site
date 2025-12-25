import asyncio

from src.config.settings import Settings
from src.infrastructure.managers.http_manager import HttpApiManager, HttpMethod


class UnisenderClient(HttpApiManager):
    def __init__(self, *, settings: Settings) -> None:
        self._api_key = settings.unisender.api_key

        super().__init__(
            base_url=settings.unisender.base_url,
            settings=settings,
        )

    async def subscribe(self, *, email: str, list_id: int) -> dict:
        return await self.send_request(
            method=HttpMethod.GET,
            endpoint="/subscribe",
            params={
                "format": "json",
                "api_key": self._api_key,
                "list_ids": list_id,
                "fields[email]": email,
                "double_optin": 3,
            },
        )

    async def bulk_subscribe(
        self,
        *,
        email: str,
        list_ids: list[int],
        return_exceptions: bool = False,
    ) -> list[dict]:
        tasks = [self.subscribe(email=email, list_id=list_id) for list_id in list_ids]

        results = await asyncio.gather(*tasks, return_exceptions=return_exceptions)
        return results
