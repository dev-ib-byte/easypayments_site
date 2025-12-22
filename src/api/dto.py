from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CommentDTO(BaseModel):
    id: int

    name: str = Field(..., max_length=250)
    email: EmailStr
    comment: str
    replay: int
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CreateCommentDTO(BaseModel):
    name: str = Field(..., max_length=250)
    email: EmailStr
    comment: str
    replay: int = 0


class UpdateCommentDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    comment: Optional[str] = None
    replay: Optional[int] = None
    active: Optional[bool] = None


class FormSubmitDTO(BaseModel):
    form: str | None = Field(default=None, max_length=250)
    status: str | None = Field(default="new", max_length=250)

    telegram: str | None = Field(default=None, max_length=250)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=250)

    description: str | None = None
    comment: str | None = None
    link: str | None = Field(default=None, max_length=1500)
    theme_request: str | None = Field(default=None, max_length=1500)
    promocode: str | None = Field(default=None, max_length=1250)
    url_form: str | None = Field(default=None, max_length=1250)

    utm_source: str | None = Field(default=None, max_length=1500)
    utm_medium: str | None = Field(default=None, max_length=1500)
    utm_campaign: str | None = Field(default=None, max_length=1500)
    utm_content: str | None = Field(default=None, max_length=1500)

    Google_id: int | None = None
    Yandex_id: int | None = None
    recaptchaToken: str | None = None


class FormOrderDTO(BaseModel):
    id: int

    form: str | None
    status: str | None

    telegram: str | None
    email: EmailStr | None
    phone: str | None

    description: str | None
    comment: str | None
    link: str | None
    theme_request: str | None
    promocode: str | None
    url_form: str | None

    utm_source: str | None
    utm_medium: str | None
    utm_campaign: str | None
    utm_content: str | None

    Google_id: int | None
    Yandex_id: int | None

    created: datetime

    class Config:
        from_attributes = True
