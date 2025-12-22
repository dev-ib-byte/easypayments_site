from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models.alchemy.base import Base


class FormOrder(Base):
    __tablename__ = "form_orders"

    form: Mapped[str | None] = mapped_column(String(250), nullable=True)
    telegram: Mapped[str | None] = mapped_column(String(250), nullable=True)
    email: Mapped[str | None] = mapped_column(String(250), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(250), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    link: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    theme_request: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    promocode: Mapped[str | None] = mapped_column(String(1250), nullable=True)
    url_form: Mapped[str | None] = mapped_column(String(1250), nullable=True)
    utm_source: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    utm_medium: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    utm_campaign: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    utm_content: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        server_default="now()",
    )


class TokenCRM(Base):
    __tablename__ = "crm_tokens"

    token: Mapped[str] = mapped_column(String(5000), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(5000), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class CommentOnline(Base):
    __tablename__ = "comments_online"

    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    replay: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        server_default="now()",
        nullable=False,
    )


class TelegramPush(Base):
    __tablename__ = "telegram_push_users"

    chat_id: Mapped[str] = mapped_column(String(500), nullable=False)
    send: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    error: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    easypay_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consult: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    buy_account: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
