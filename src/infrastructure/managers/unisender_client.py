from src.config.settings import Settings
from src.infrastructure.managers.http_manager import HttpApiManager, HttpMethod


class UnisenderClient(HttpApiManager):
    def __init__(self, *, settings: Settings) -> None:
        super().__init__(
            base_url=settings.unisender.base_url,
            settings=settings,
        )

    def subscribe(self, *, email: str, list_id: int) -> None:
        self.send_request(
            method=HttpMethod.POST,
            endpoint="/ru/api/subscribe",
            json={
                "list_ids": [list_id],
                "fields": {"email": email},
                "overwrite": 2,
            },
        )
