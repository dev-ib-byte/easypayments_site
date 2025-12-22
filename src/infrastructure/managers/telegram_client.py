import httpx

from src.config.settings import Settings


class TelegramClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.base_url = f"https://api.telegram.org/bot{settings.telegram.token}"

    async def send_message(self, *, chat_id: int, text: str) -> None:
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
