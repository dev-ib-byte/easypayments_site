from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.entities.enums import ModelType
from src.infrastructure.repositories.interfaces.base import ModelRepository
from src.infrastructure.uow.base import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._session_factory()

        # self.users = SqlAlchemyUsersRepository(self._session)

        return await super().__aenter__()

    def get_model_repository(self, model_name: ModelType) -> ModelRepository:
        match model_name:
            case ModelType.USERS:
                return self.users
            case _:
                raise ValueError(f"Repository not found: {model_name}")

    async def rollback(self) -> None:
        await self._session.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    async def shutdown(self) -> None:
        await self._session.close()
