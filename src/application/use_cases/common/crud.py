from typing import Any, Type, TypeVar

from fastapi import Request
from pydantic import BaseModel

from src.domain.entities.enums import ModelType
from src.domain.validators.dto import PaginatedResponse
from src.infrastructure.managers.paginator import Paginator
from src.infrastructure.uow import UnitOfWork

TRead = TypeVar("TRead", bound=BaseModel)
TWrite = TypeVar("TWrite", bound=BaseModel)


class CRUDUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def list(
        self,
        *,
        request: Request,
        model_type: ModelType,
        read_dto: Type[TRead],
        page: int,
        page_size: int,
        filters: dict[str, Any] | None = None,
    ) -> PaginatedResponse[TRead]:
        async with self.uow(autocommit=True):
            repo = self.uow.get_model_repository(model_type)
            data = await repo.get_list_models(**(filters or {}))

        return await Paginator(read_dto).paginate(
            data,
            request,
            page,
            page_size,
        )

    async def retrieve(
        self,
        *,
        model_type: ModelType,
        obj_id: int,
        read_dto: Type[TRead],
    ) -> TRead:
        async with self.uow(autocommit=True):
            repo = self.uow.get_model_repository(model_type)
            obj = await repo.get_by_id(obj_id)

        return read_dto.model_validate(obj)

    async def create(
        self,
        *,
        model_type: ModelType,
        data: TWrite,
        read_dto: Type[TRead],
    ) -> TRead:
        async with self.uow():
            entity_cls = self.uow.get_model_entity(model_type)
            repo = self.uow.get_model_repository(model_type)
            obj = await repo.create(entity_cls(**data.model_dump()))

        return read_dto.model_validate(obj)

    async def update(
        self,
        *,
        model_type: ModelType,
        obj_id: int,
        data: TWrite,
        read_dto: Type[TRead],
    ) -> TRead:
        async with self.uow(autocommit=True):
            repo = self.uow.get_model_repository(model_type)

            entity = await repo.get_by_id(obj_id)
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(entity, field, value)

            entity = await repo.update(entity)

        return read_dto.model_validate(entity)

    async def delete(
        self,
        *,
        model_type: ModelType,
        obj_id: int,
    ) -> None:
        async with self.uow():
            repo = self.uow.get_model_repository(model_type)
            await repo.delete_by_id(obj_id)
