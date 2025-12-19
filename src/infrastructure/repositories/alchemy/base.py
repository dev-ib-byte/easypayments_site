from typing import Any, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Result, and_, delete, exists, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import APIException
from src.domain.entities.model import Model
from src.infrastructure.models.alchemy.base import Base
from src.infrastructure.repositories.interfaces.base import ModelRepository, Repository

TModel = TypeVar("TModel", bound=Model)


class SqlAlchemyRepository(Repository):
    MODEL: Type[Base]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session


class SqlAlchemyModelRepository(SqlAlchemyRepository, ModelRepository[TModel]):
    ENTITY: Type[Model]
    LIST_DTO: Type[BaseModel]

    ###############
    ### Getters ###
    ###############

    async def get_by_id(self, model_id: int, **filters: Any) -> TModel:
        stmt = select(self.MODEL).filter_by(id=model_id).filter_by(**filters)
        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()
        if not model:
            raise APIException(
                code=404,
                message=f"Объект модели `{self.MODEL.__tablename__}` c id={model_id} не найден",
            )
        return self.convert_to_entity(model)

    async def get_list(
        self,
        per_page: int | None = None,
        page: int | None = None,
    ) -> list:
        stmt = select(self.MODEL)

        if page and per_page:
            stmt = stmt.limit(per_page).offset((page - 1) * per_page)

        result = await self._session.scalars(stmt.order_by(getattr(self.MODEL, "id").desc()))

        objects = result.all()
        return [self.LIST_DTO.model_validate(obj) for obj in objects]

    async def get_list_models(self, **filters: Any) -> Result:
        stmt = select(self.MODEL).filter_by(**filters)
        result = await self._session.execute(stmt)
        return result

    ################
    ### Creators ###
    ################

    async def create(self, data: TModel) -> TModel:
        model = self.convert_to_model(data)
        self._session.add(model)
        await self._session.flush()
        return self.convert_to_entity(model)

    async def bulk_create(self, data: list[TModel]) -> list[TModel]:
        models = [self.convert_to_model(entity) for entity in data]
        self._session.add_all(models)
        await self._session.flush(models)
        return [self.convert_to_entity(model) for model in models]

    ################
    ### Updators ###
    ################

    async def update(self, data: TModel) -> None:
        await self.bulk_update([data])

    async def bulk_update(self, entities: list[TModel]) -> None:
        models = [self.convert_to_model(entity) for entity in entities]

        for model in models:
            data = {
                col.name: getattr(model, col.name)
                for col in self.MODEL.__table__.columns
                if getattr(model, col.name) is not None
            }

            # Выполняем UPDATE по первичному ключу
            await self._session.execute(update(self.MODEL).where(self.MODEL.id == model.id).values(**data))

    ################
    ### Deleters ###
    ################
    async def delete_by_id(self, model_id: int) -> None:
        model = await self._session.get(self.MODEL, model_id)
        if not model:
            raise APIException(
                code=404,
                message=f"Объект модели `{self.MODEL.__tablename__}` c id={model_id} не найден",
            )
        await self._session.delete(model)
        await self._session.flush()

    async def delete_all(self, scenario_id: int) -> None:
        await self._session.execute(
            delete(self.MODEL).filter(getattr(self.MODEL, "scenario_id") == scenario_id)
        )

    async def delete(self, id_list: list[int]) -> list[int]:
        delete_query = delete(self.MODEL).where(self.MODEL.id.in_(id_list))
        await self._session.execute(delete_query)
        return id_list

    async def exists(self, **filters) -> bool:
        """Проверяет, существует ли объект с заданными параметрами"""
        conditions = [getattr(self.MODEL, field) == value for field, value in filters.items()]
        stmt = select(exists().where(and_(*conditions)))

        result = await self._session.execute(stmt)
        return result.scalar()

    async def all_exist_by_id_list(self, id_lst: list) -> bool:
        """Проверяет, существуют ли все объекты из списка id"""
        if not id_lst:
            return False

        stmt = select(func.count(self.MODEL.id)).where(self.MODEL.id.in_(id_lst))
        result = await self._session.scalar(stmt)
        return result == len(id_lst)
