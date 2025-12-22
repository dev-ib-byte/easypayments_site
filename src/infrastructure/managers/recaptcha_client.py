from src.config.settings import Settings
from src.infrastructure.managers.http_manager import HttpApiManager, HttpMethod


class RecaptchaClient(HttpApiManager):
    def __init__(self, *, settings: Settings) -> None:
        super().__init__(
            base_url=settings.recaptcha.base_url,
            settings=settings,
        )

    def verify(self, *, token: str, remote_ip: str | None = None) -> bool:
        params = {
            "secret": self.settings.recaptcha.secret_key,
            "response": token,
        }

        if remote_ip:
            params["remoteip"] = remote_ip

        response = self.send_request(
            method=HttpMethod.POST,
            endpoint="/siteverify",
            params=params,
        )

        return bool(response.get("success"))
