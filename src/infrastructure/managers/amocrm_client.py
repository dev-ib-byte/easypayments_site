from typing import Any, Awaitable, Callable

from sqlalchemy import select, update

from src.config.settings import Settings
from src.infrastructure.managers.http_manager import HttpApiManager, HttpMethod
from src.infrastructure.models.alchemy.forms import TokenCRM
from src.infrastructure.uow import SqlAlchemyUnitOfWork


class AmoCRMClient(HttpApiManager):
    def __init__(self, *, settings: Settings) -> None:
        super().__init__(base_url=settings.amocrm.base_url, settings=settings)

        self.client_id = settings.amocrm.client_id
        self.client_secret = settings.amocrm.client_secret
        self.redirect_uri = settings.amocrm.redirect_uri
        self._settings_refresh_token = settings.amocrm.refresh_token

        self.access_token: str | None = None
        self.refresh_token: str | None = None

    async def init_tokens(self, uow: SqlAlchemyUnitOfWork) -> None:
        async with uow():
            result = await uow.session.execute(select(TokenCRM).where(TokenCRM.active.is_(True)))
            token_row = result.scalar_one_or_none()

            if token_row:
                self.access_token = token_row.token
                self.refresh_token = token_row.refresh_token
                return

        await self._refresh_and_persist(uow, self._settings_refresh_token)

    async def create_lead(self, data: list[dict[str, Any]], uow: SqlAlchemyUnitOfWork) -> Any:
        return await self._safe_request(
            uow=uow,
            request=lambda: self.send_request(
                method=HttpMethod.POST,
                endpoint="/api/v4/leads",
                json=data,
            ),
        )

    async def create_contact(self, data: list[dict[str, Any]], uow: SqlAlchemyUnitOfWork) -> Any:
        return await self._safe_request(
            uow=uow,
            request=lambda: self.send_request(
                method=HttpMethod.POST,
                endpoint="/api/v4/contacts",
                json=data,
            ),
        )

    async def link_lead_to_contact(
        self,
        *,
        lead_id: int,
        contact_id: int,
        uow: SqlAlchemyUnitOfWork,
    ) -> Any:
        return await self._safe_request(
            uow=uow,
            request=lambda: self.send_request(
                method=HttpMethod.POST,
                endpoint=f"/api/v4/leads/{lead_id}/link",
                json=[
                    {
                        "to_entity_id": contact_id,
                        "to_entity_type": "contacts",
                        "metadata": {"is_main": True},
                    }
                ],
            ),
        )

    async def _safe_request(
        self,
        *,
        uow: SqlAlchemyUnitOfWork,
        request: Callable[[], Awaitable[Any]],
    ) -> Any:
        try:
            return await request()
        except Exception as exc:
            if self._is_403(exc):
                await self._refresh_and_persist(uow, self.refresh_token)
                return await request()
            raise

    async def _refresh_and_persist(
        self,
        uow: SqlAlchemyUnitOfWork,
        refresh_token: str,
    ) -> None:
        json = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = await self.send_request(
            method=HttpMethod.POST, endpoint="/oauth2/access_token", json=json
        )

        self.access_token = response["access_token"]
        self.refresh_token = response["refresh_token"]

        async with uow():
            await uow.session.execute(update(TokenCRM).values(active=False))
            uow.session.add(
                TokenCRM(
                    token=self.access_token,
                    refresh_token=self.refresh_token,
                    active=True,
                )
            )

    @staticmethod
    def _is_403(exc: Exception) -> bool:
        return "403" in str(exc)
