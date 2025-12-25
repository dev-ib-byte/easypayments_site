from src.config.settings import Settings
from src.infrastructure.managers.http_manager import HttpApiManager, HttpMethod


class RecaptchaClient(HttpApiManager):
    def __init__(self, *, settings: Settings) -> None:
        super().__init__(
            base_url=settings.recaptcha.base_url,
            settings=settings,
        )

    async def verify(self, *, token: str, remote_ip: str | None = None) -> bool:
        session = await self._get_session()

        data = {
            "secret": self.settings.recaptcha.secret_key,
            "response": token,
        }
        if remote_ip:
            data["remoteip"] = remote_ip

        async with session.post(f"{self.base_url}/siteverify", data=data) as response:
            payload = await response.json()
            return bool(payload.get("success"))
