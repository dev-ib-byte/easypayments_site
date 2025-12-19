from typing import Any

from src.config.settings import Settings
from src.infrastructure.managers.http_manager import HttpMethod, HttpApiManager


class AmoCRMClient(HttpApiManager):
    def __init__(self, *, refresh_token: str) -> None:
        self.access_token = None
        settings = Settings().amocrm

        super().__init__(
            base_url=settings.base_url,
            access_token=None,
        )

        self.client_id = settings.client_id
        self.client_secret = settings.client_secret
        self.redirect_uri = settings.redirect_uri
        self.refresh_token = refresh_token

    def authenticate(self) -> str:
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

        return self.refresh_token

    def create_lead(self, lead_data: dict[str, Any]) -> Any:
        return self.send_request(
            method=HttpMethod.POST,
            endpoint="/api/v4/leads",
            json=lead_data,
        )

    def create_contact(self, contact_data: dict[str, Any]) -> Any:
        return self.send_request(
            method=HttpMethod.POST,
            endpoint="/api/v4/contacts",
            json=contact_data,
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
