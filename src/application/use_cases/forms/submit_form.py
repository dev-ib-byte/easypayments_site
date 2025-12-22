import asyncio

from src.api.dto import FormSubmitDTO
from src.application.builders import build_contact_data, build_lead_data
from src.application.constants import (
    forms_to_lists_mapper,
    forms_to_pipelines_mapper,
)
from src.common.exceptions import APIException
from src.domain.entities.enums import ModelType
from src.domain.entities.form_order import FormOrder
from src.infrastructure.managers.amocrm_client import AmoCRMClient
from src.infrastructure.managers.recaptcha_client import RecaptchaClient
from src.infrastructure.managers.telegram_client import TelegramClient
from src.infrastructure.managers.unisender_client import UnisenderClient
from src.infrastructure.uow import UnitOfWork


class SubmitFormUseCase:
    def __init__(
        self,
        *,
        uow: UnitOfWork,
        recaptcha_client: RecaptchaClient,
        unisender_client: UnisenderClient,
        telegram_client: TelegramClient,
        amocrm_client: AmoCRMClient,
    ) -> None:
        self.uow = uow
        self._recaptcha = recaptcha_client
        self._unisender = unisender_client
        self._telegram = telegram_client
        self._amocrm = amocrm_client

    async def execute(
        self,
        data: FormSubmitDTO,
        client_ip: str | None = None,
    ) -> FormOrder:
        payload = data.model_dump()

        if not payload.get("email"):
            raise APIException(code=400, message="Missing email")

        payload["Google_id"] = self._normalize_counter(payload.get("Google_id"))
        payload["Yandex_id"] = self._normalize_counter(payload.get("Yandex_id"))

        self._validate_recaptcha(
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

        async with self.uow():
            repo = self.uow.get_model_repository(ModelType.FORM_ORDERS)
            created = await repo.create(entity)

        await self._notify(created)
        self._send_to_marketing(created)
        self._send_to_crm(created)

        return created

    # ==========================
    # helpers (из Django)
    # ==========================

    def _normalize_counter(self, value) -> int:
        if value in (None, "", False):
            return 0
        try:
            return int(value)
        except Exception:
            return 0

    def _truncate(self, value: str | None, limit: int = 240) -> str | None:
        if not value:
            return None
        if len(value) <= limit:
            return value
        return value[: limit - 10] + "..."

    def _validate_recaptcha(self, token: str | None, client_ip: str | None) -> None:
        if not token:
            return

        ok = self._recaptcha.verify(
            token=token,
            remote_ip=client_ip,
        )
        if not ok:
            raise APIException(code=403, message="Invalid reCAPTCHA")


    async def _notify(self, entity: FormOrder) -> None:
        text = f"""
                💥 <b>Новая заявка</b>
                
                <b>Форма:</b> {entity.form}
                <b>Email:</b> {entity.email}
                <b>Телефон:</b> {entity.phone}
                <b>Telegram:</b> {entity.telegram}
                
                <b>Комментарий:</b>
                {entity.comment}
                
                <b>UTM:</b>
                source: {entity.utm_source}
                medium: {entity.utm_medium}
                campaign: {entity.utm_campaign}
                content: {entity.utm_content}
            """

        tasks = [
            self._telegram.send_message(chat_id=chat_id, text=text)
            for chat_id in self._telegram.settings.telegram.chat_ids
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

    def _send_to_marketing(self, entity: FormOrder) -> None:
        lists = forms_to_lists_mapper.get(entity.form, [])
        for list_id in lists:
            self._unisender.subscribe(
                email=entity.email,
                list_id=list_id,
            )

    def _send_to_crm(self, entity: FormOrder) -> None:
        pipeline = forms_to_pipelines_mapper.get(entity.form)
        if not pipeline:
            return

        self._amocrm.authenticate()

        lead_data = build_lead_data(entity, pipeline)
        contact_data = build_contact_data(entity)

        lead_resp = self._amocrm.create_lead(lead_data)
        contact_resp = self._amocrm.create_contact(contact_data)

        lead_id = lead_resp["_embedded"]["leads"][0]["id"]
        contact_id = contact_resp["_embedded"]["contacts"][0]["id"]

        self._amocrm.link_lead_to_contact(
            lead_id=lead_id,
            contact_id=contact_id,
        )
