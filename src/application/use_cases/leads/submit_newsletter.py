from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from sqlalchemy import insert, select

from src.application.constants import EASY_PAYMENTS_SUBSCRIPTION
from src.application.messages.telegram import SUBSCRIPTION
from src.infrastructure.managers.telegram_client import TelegramClient
from src.infrastructure.managers.unisender_client import UnisenderClient
from src.infrastructure.models.alchemy.forms import Newsletter, TelegramPush
from src.infrastructure.uow import SqlAlchemyUnitOfWork

if TYPE_CHECKING:
    from src.api.dto import NewsletterDTO


class NewsletterSubmitUseCase:
    def __init__(
        self,
        *,
        uow: SqlAlchemyUnitOfWork,
        unisender: UnisenderClient,
        telegram: TelegramClient,
    ) -> None:
        self._uow = uow
        self._unisender = unisender
        self._telegram = telegram

    async def execute(self, data: NewsletterDTO) -> None:
        async with self._uow():
            await self._uow.session.execute(
                insert(Newsletter).values(
                    email=data.email,
                    form=data.form,
                )
            )
            result = await self._uow.session.execute(
                select(TelegramPush.chat_id).where(TelegramPush.send.is_(True))
            )
            chat_ids = result.scalars().all()

        self._unisender.subscribe(email=data.email, list_id=EASY_PAYMENTS_SUBSCRIPTION)

        text = SUBSCRIPTION.format(**self.newsletter_context(data))

        await self._telegram.broadcast(text, chat_ids)

    @staticmethod
    def newsletter_context(data: NewsletterDTO) -> dict[str, str]:
        return {
            "email": data.email or "-",
            "form": data.form or "-",
            "utm_source": data.utm_source or "-",
            "utm_medium": data.utm_medium or "-",
            "utm_campaign": data.utm_campaign or "-",
            "utm_content": data.utm_content or "-",
            "url_form": quote(data.url_form or ""),
        }
