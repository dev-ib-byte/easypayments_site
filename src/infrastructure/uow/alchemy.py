from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.entities.comment import Comment
from src.domain.entities.entity import Entity
from src.domain.entities.enums import ModelType
from src.domain.entities.form_order import FormOrder
from src.domain.entities.telegram_push import TelegramPush
from src.infrastructure.repositories.alchemy.comments import SqlAlchemyCommentsRepository
from src.infrastructure.repositories.alchemy.form_orders import SqlAlchemyFormOrderRepository
from src.infrastructure.repositories.alchemy.telegram_pushes import SqlAlchemyTelegramPushRepository
from src.infrastructure.repositories.interfaces.base import ModelRepository
from src.infrastructure.uow.base import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        self.comments = SqlAlchemyCommentsRepository(self._session)
        self.forms = SqlAlchemyFormOrderRepository(self._session)
        self.pushes = SqlAlchemyTelegramPushRepository(self._session)

        return await super().__aenter__()

    def get_model_repository(self, model_name: ModelType) -> ModelRepository:
        match model_name:
            case ModelType.COMMENTS:
                return self.comments
            case ModelType.FORM_ORDERS:
                return self.forms
            case ModelType.TELEGRAM_PUSH_USERS:
                return self.pushes
            case _:
                raise ValueError(f"Repository not found: {model_name}")

    def get_model_entity(self, model_name: ModelType) -> Type[Entity]:
        match model_name:
            case ModelType.COMMENTS:
                return Comment
            case ModelType.FORM_ORDERS:
                return FormOrder
            case ModelType.TELEGRAM_PUSH_USERS:
                return TelegramPush
            case _:
                raise ValueError(f"Repository not found: {model_name}")

    async def rollback(self) -> None:
        await self._session.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    async def shutdown(self) -> None:
        await self._session.close()

    @property
    def session(self):
        return self._session
