from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

from sqlalchemy import Result

from src.domain.entities.entity import Entity
from src.domain.entities.model import Model

TModel = TypeVar("TModel", bound=Entity)


class Repository(ABC):
    @abstractmethod
    def convert_to_model(self, entity: Any) -> Any:
        pass

    @abstractmethod
    def convert_to_entity(self, model: Any) -> Any:
        pass


class ModelRepository(Repository, Generic[TModel]):
    ENTITY: Type[Model]

    @abstractmethod
    def convert_to_model(self, entity: TModel) -> Any:
        pass

    @abstractmethod
    def convert_to_entity(self, model: Any) -> TModel:
        pass

    @abstractmethod
    async def create(self, data: TModel) -> TModel:
        pass

    @abstractmethod
    async def bulk_create(self, data: list[TModel]) -> list[TModel]:
        pass

    @abstractmethod
    async def get_by_id(self, model_id: int) -> TModel:
        pass

    @abstractmethod
    async def get_list(
        self,
        per_page: int | None = None,
        page: int | None = None,
    ) -> list[TModel]:
        pass

    @abstractmethod
    async def get_list_models(self, **filters) -> Result:
        pass

    @abstractmethod
    async def update(self, data: TModel) -> TModel:
        pass

    @abstractmethod
    async def bulk_update(self, entities: list[TModel]) -> None:
        pass

    @abstractmethod
    async def delete(self, id_list: list[int]) -> list[int]:
        pass

    @abstractmethod
    async def delete_by_id(self, model_id: int) -> None:
        pass

    @abstractmethod
    async def delete_all(self, scenario_id: int) -> None:
        pass

    @abstractmethod
    async def exists(self, **filters) -> bool:
        pass
