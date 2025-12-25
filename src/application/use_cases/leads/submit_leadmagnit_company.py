from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from sqlalchemy import insert, select

from src.application.constants import EP_REQ_ALL, EP_REQ_LEAD_COMP
from src.application.messages.telegram import LEAD_MAGNIT_COMPANY
from src.application.use_cases.leads.submit_leadmagnit import LeadMagnitSubmitUseCase
from src.infrastructure.models.alchemy.forms import LeadMagnit, TelegramPush

if TYPE_CHECKING:
    from src.api.dto import LeadMagnitDTO


class LeadMagnitCompanySubmitUseCase(LeadMagnitSubmitUseCase):
    async def execute(self, data: LeadMagnitDTO) -> None:
        async with self._uow():
            await self._uow.session.execute(insert(LeadMagnit).values(email=data.email))

            result = await self._uow.session.execute(
                select(TelegramPush.chat_id).where(TelegramPush.send.is_(True))
            )
            chat_ids = result.scalars().all()

        self._unisender.subscribe(email=data.email, list_id=EP_REQ_LEAD_COMP)
        self._unisender.subscribe(email=data.email, list_id=EP_REQ_ALL)

        text = LEAD_MAGNIT_COMPANY.format(**self.lead_magnit_context(data))

        await self._telegram.broadcast(text, chat_ids)

    @staticmethod
    def lead_magnit_context(data: LeadMagnitDTO) -> dict[str, str]:
        return {
            "email": data.email or "-",
            "utm_source": data.utm_source or "-",
            "utm_medium": data.utm_medium or "-",
            "utm_campaign": data.utm_campaign or "-",
            "utm_content": data.utm_content or "-",
            "url_form": quote(data.url_form or ""),
        }
