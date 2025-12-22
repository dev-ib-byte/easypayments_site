from datetime import datetime

from src.domain.entities.entity import Entity


class FormOrder(Entity):
    def __init__(
        self,
        id: int | None = None,
        form: str | None = None,
        status: str | None = "new",
        telegram: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        description: str | None = None,
        comment: str | None = None,
        link: str | None = None,
        theme_request: str | None = None,
        promocode: str | None = None,
        url_form: str | None = None,
        utm_source: str | None = None,
        utm_medium: str | None = None,
        utm_campaign: str | None = None,
        utm_content: str | None = None,
        created: datetime | None = None,
    ) -> None:
        super().__init__(id)

        self.form = form
        self.status = status

        self.telegram = telegram
        self.email = email
        self.phone = phone

        self.description = description
        self.comment = comment
        self.link = link
        self.theme_request = theme_request
        self.promocode = promocode
        self.url_form = url_form

        self.utm_source = utm_source
        self.utm_medium = utm_medium
        self.utm_campaign = utm_campaign
        self.utm_content = utm_content

        self.created = created or datetime.now()
