from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from sqlalchemy import insert

from src.infrastructure.managers.telegram_client import TelegramClient
from src.infrastructure.managers.unisender_client import UnisenderClient
from src.infrastructure.models.alchemy.forms import Newsletter
from src.infrastructure.uow import SqlAlchemyUnitOfWork

if TYPE_CHECKING:
    from src.api.dto import NewsletterDTO

from src.application.constants import EASY_PAYMENTS_SUBSCRIPTION


class NewsletterSubmitUseCase:
    def __init__(
        self,
        *,
        uow: SqlAlchemyUnitOfWork,
        unisender: UnisenderClient,
        telegram: TelegramClient,
    ) -> None:
        self.uow = uow
        self._unisender = unisender
        self._telegram = telegram

    async def execute(self, data: NewsletterDTO) -> None:
        async with self.uow():
            await self.uow.session.execute(
                insert(Newsletter).values(
                    email=data.email,
                    form=data.form,
                )
            )

        self._unisender.subscribe(email=data.email, list_id=EASY_PAYMENTS_SUBSCRIPTION)

        text = f"""
            💥<b>Подписка на рассылку</b>:
            Email: {data.email}
            Form: {data.form}
            
            ***********************
            utm_source: {data.utm_source}
            utm_medium: {data.utm_medium}
            utm_campaign: {data.utm_campaign}
            utm_content: {data.utm_content}
            Страница: {quote(data.url_form or "")}
        """

        await self._telegram.broadcast(text)
