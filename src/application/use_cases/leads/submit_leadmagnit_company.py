from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from sqlalchemy import insert

from src.application.constants import EP_REQ_ALL
from src.application.use_cases.leads.submit_leadmagnit import LeadMagnitSubmitUseCase
from src.domain.entities.leadmagnit import LeadMagnit

if TYPE_CHECKING:
    from src.api.dto import LeadMagnitDTO


class LeadMagnitCompanySubmitUseCase(LeadMagnitSubmitUseCase):
    async def execute(self, data: LeadMagnitDTO) -> None:
        async with self._uow():
            await self._uow.session.execute(insert(LeadMagnit).values(email=data.email))

        self._unisender.subscribe(email=data.email, list_id=EP_REQ_LEAD_COMP)
        self._unisender.subscribe(email=data.email, list_id=EP_REQ_ALL)

        text = f"""
            💥<b>LeadMagnit Компании</b>:
            Email: {data.email}
            
            ***********************
            utm_source: {data.utm_source}
            utm_medium: {data.utm_medium}
            utm_campaign: {data.utm_campaign}
            utm_content: {data.utm_content}
            Страница: {quote(data.url_form or "")}
        """

        await self._telegram.broadcast(text)
