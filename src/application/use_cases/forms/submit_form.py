from __future__ import annotations

import json
from typing import TYPE_CHECKING

from sqlalchemy import select

from src.application.builders import build_contact_data, build_lead_data
from src.application.constants import (
    forms_to_lists_mapper,
    forms_to_pipelines_mapper,
)
from src.application.messages.telegram import ERROR_MESSAGE, NEW_FORM_ORDER
from src.common.exceptions import APIException
from src.domain.entities.enums import ModelType
from src.domain.entities.form_order import FormOrder
from src.infrastructure.managers.amocrm_client import AmoCRMClient
from src.infrastructure.managers.recaptcha_client import RecaptchaClient
from src.infrastructure.managers.telegram_client import TelegramClient
from src.infrastructure.managers.unisender_client import UnisenderClient
from src.infrastructure.models.alchemy.forms import TelegramPush
from src.infrastructure.uow import SqlAlchemyUnitOfWork

if TYPE_CHECKING:
    from src.api.dto import FormOrderDTO, FormSubmitDTO


class SubmitFormUseCase:
    def __init__(
        self,
        *,
        uow: SqlAlchemyUnitOfWork,
        recaptcha_client: RecaptchaClient,
        unisender_client: UnisenderClient,
        telegram_client: TelegramClient,
        amocrm_client: AmoCRMClient,
    ) -> None:
        self._uow = uow
        self._recaptcha = recaptcha_client
        self._unisender = unisender_client
        self._telegram = telegram_client
        self._amocrm = amocrm_client

    async def execute(
        self,
        data: FormSubmitDTO,
        client_ip: str | None = None,
    ) -> FormOrderDTO:
        from src.api.dto import FormOrderDTO

        payload = data.model_dump()

        if not payload.get("email"):
            raise APIException(code=400, message="Missing email")

        payload["Google_id"] = self._normalize_counter(payload.get("Google_id"))
        payload["Yandex_id"] = self._normalize_counter(payload.get("Yandex_id"))

        await self._validate_recaptcha(
            token=payload.get("recaptchaToken"),
            client_ip=client_ip,
        )

        entity = FormOrder(
            form=payload.get("form"),
            telegram=payload.get("telegram"),
            email=payload.get("email"),
            phone=payload.get("phone"),
            description=self._truncate(payload.get("description")),
            comment=self._truncate(payload.get("comment")),
            link=self._truncate(payload.get("link")),
            theme_request=payload.get("theme_request"),
            promocode=payload.get("promocode"),
            url_form=self._truncate(payload.get("url_form")),
            utm_source=payload.get("utm_source"),
            utm_medium=payload.get("utm_medium"),
            utm_campaign=payload.get("utm_campaign"),
            utm_content=payload.get("utm_content"),
        )

        async with self._uow():
            repo = self._uow.get_model_repository(ModelType.FORM_ORDERS)
            created = await repo.create(entity)

        await self._notify(created)
        await self._send_to_marketing(created)
        await self._send_to_crm(created)

        return FormOrderDTO.model_validate(created)

    @staticmethod
    def _normalize_counter(value) -> int:
        if value in (None, "", False):
            return 0
        try:
            return int(value)
        except ValueError:
            return 0

    @staticmethod
    def _truncate(value: str | None, limit: int = 240) -> str | None:
        if not value:
            return None
        if len(value) <= limit:
            return value
        return value[: limit - 10] + "..."

    async def _validate_recaptcha(self, token: str | None, client_ip: str | None) -> None:
        if not token:
            return

        ok = await self._recaptcha.verify(
            token=token,
            remote_ip=client_ip,
        )
        if not ok:
            raise APIException(code=403, message="Invalid reCAPTCHA")

    async def _notify(self, entity: FormOrder) -> None:
        context = self.form_order_context(entity)
        text = NEW_FORM_ORDER.format(**context)

        async with self._uow():
            result = await self._uow.session.execute(
                select(TelegramPush.chat_id).where(TelegramPush.send.is_(True))
            )
            chat_ids = result.scalars().all()

        await self._telegram.broadcast(chat_ids=chat_ids, text=text)

    async def _send_to_marketing(self, entity: FormOrder) -> None:
        try:
            await self._unisender.bulk_subscribe(
                email=entity.email,
                list_ids=forms_to_lists_mapper.get(entity.form, []),
            )
        except Exception as e:
            await self._send_error_notification(str(e))

    async def _send_to_crm(self, entity: FormOrder) -> None:
        pipeline = forms_to_pipelines_mapper.get(entity.form)
        if not pipeline:
            return

        try:
            await self._amocrm.init_tokens(self._uow)

            lead_data = build_lead_data(entity, pipeline)
            contact_data = build_contact_data(entity)

            lead_resp = await self._amocrm.create_lead(lead_data, self._uow)
            contact_resp = await self._amocrm.create_contact(contact_data, self._uow)

            lead_id = json.loads(lead_resp)["_embedded"]["leads"][0]["id"]
            contact_id = json.loads(contact_resp)["_embedded"]["contacts"][0]["id"]

            await self._amocrm.link_lead_to_contact(lead_id=lead_id, contact_id=contact_id, uow=self._uow)
        except Exception as e:
            await self._send_error_notification(str(e))

    async def _send_error_notification(self, error: str = "") -> None:
        text = ERROR_MESSAGE.format(error=error)
        async with self._uow():
            result = await self._uow.session.execute(
                select(TelegramPush.chat_id).where(TelegramPush.send.is_(True))
            )
            chat_ids = result.scalars().all()

        await self._telegram.broadcast(chat_ids=chat_ids, text=text)

    @staticmethod
    def form_order_context(entity: FormOrder) -> dict[str, str]:
        return {
            "form": entity.form or "-",
            "email": entity.email or "-",
            "phone": entity.phone or "-",
            "telegram": entity.telegram or "-",
            "comment": entity.comment or "-",
            "utm_source": entity.utm_source or "-",
            "utm_medium": entity.utm_medium or "-",
            "utm_campaign": entity.utm_campaign or "-",
            "utm_content": entity.utm_content or "-",
        }
