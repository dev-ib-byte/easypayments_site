from typing import Any

from src.config.settings import Settings
from src.infrastructure.managers.http_manager import HttpApiManager, HttpMethod


class AmoCRMClient(HttpApiManager):
    def __init__(self, *, settings: Settings) -> None:
        super().__init__(
            base_url=settings.amocrm.base_url,
            settings=settings,
        )

        self.client_id = settings.amocrm.client_id
        self.client_secret = settings.amocrm.client_secret
        self.redirect_uri = settings.amocrm.redirect_uri
        self.refresh_token = settings.amocrm.refresh_token

    def authenticate(self) -> None:
        response = self.send_request(
            method=HttpMethod.POST,
            endpoint="/oauth2/access_token",
            json={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "redirect_uri": self.redirect_uri,
            },
        )

        self.access_token = response["access_token"]
        self.refresh_token = response["refresh_token"]

    def create_lead(self, data: list[dict[str, Any]]) -> Any:
        return self.send_request(
            method=HttpMethod.POST,
            endpoint="/api/v4/leads",
            json=data,
        )

    def create_contact(self, data: list[dict[str, Any]]) -> Any:
        return self.send_request(
            method=HttpMethod.POST,
            endpoint="/api/v4/contacts",
            json=data,
        )

    def link_lead_to_contact(self, *, lead_id: int, contact_id: int) -> Any:
        return self.send_request(
            method=HttpMethod.POST,
            endpoint=f"/api/v4/leads/{lead_id}/link",
            json=[
                {
                    "to_entity_id": contact_id,
                    "to_entity_type": "contacts",
                    "metadata": {"is_main": True},
                }
            ],
        )
