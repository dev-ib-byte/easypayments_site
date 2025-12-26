from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Type

from src.domain.entities.entity import Entity
from src.domain.entities.enums import ModelType
from src.infrastructure.repositories.alchemy.comments import SqlAlchemyCommentsRepository
from src.infrastructure.repositories.alchemy.form_orders import SqlAlchemyFormOrderRepository
from src.infrastructure.repositories.alchemy.telegram_pushes import SqlAlchemyTelegramPushRepository
from src.infrastructure.repositories.interfaces.base import ModelRepository


class UnitOfWork(ABC):
    comments: SqlAlchemyCommentsRepository
    forms: SqlAlchemyFormOrderRepository
    pushes: SqlAlchemyTelegramPushRepository

    def __call__(self, *args: Any, autocommit: bool = True, **kwargs: Any) -> "UnitOfWork":
        self._autocommit = autocommit
        return self

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        elif self._autocommit:
            await self.commit()
        await self.shutdown()

    @abstractmethod
    def get_model_repository(self, model_name) -> ModelRepository:
        pass

    @abstractmethod
    def get_model_entity(self, model_name: ModelType) -> Type[Entity]:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass
