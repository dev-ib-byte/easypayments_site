import asyncio
from typing import Iterable

import httpx

from src.config.settings import Settings


class TelegramClient:
    def __init__(self, settings: Settings) -> None:
        self._token = settings.telegram.token
        self._base_url = f"https://api.telegram.org/bot{self._token}"

        self._timeout = httpx.Timeout(
            connect=20.0,
            read=20.0,
            write=20.0,
            pool=20.0,
        )

        self._client = httpx.AsyncClient(timeout=self._timeout)

    async def close(self) -> None:
        await self._client.aclose()

    async def broadcast(self, text: str, chat_ids: Iterable[int | str]) -> None:
        tasks = [self._send_message(chat_id=chat_id, text=text) for chat_id in chat_ids if chat_id]

        if not tasks:
            return

        await asyncio.gather(*tasks, return_exceptions=True)

    async def send_message(self, chat_id: int | str, text: str) -> bool:
        if not chat_id:
            return False

        return await self._send_message(chat_id=chat_id, text=text)

    async def _send_message(self, chat_id: int | str, text: str) -> bool:
        url = f"{self._base_url}/sendMessage"

        try:
            response = await self._client.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                },
            )

            if response.status_code != 200:
                try:
                    error = response.json()
                except Exception:
                    error = response.text

                return False

            data = response.json()
            return bool(data.get("ok"))

        except httpx.RequestError as exc:
            return False
