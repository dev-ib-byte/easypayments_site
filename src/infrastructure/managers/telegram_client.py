import httpx

from src.config.settings import Settings


class TelegramClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self.base_url = f"{self._settings.telegram.base_url}{settings.telegram.token}"

    async def broadcast(self, text: str, chat_ids: list[str]) -> None:
        for chat_id in chat_ids:
            await self.send_message(chat_id, text)

    async def send_message(self, chat_id: str, text: str) -> None:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                },
            )
            response.raise_for_status()
