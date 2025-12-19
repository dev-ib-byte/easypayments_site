from typing import Type, TypeVar

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request, status
from pydantic import BaseModel

from src.application.use_cases.common.crud import CRUDUseCase
from src.config.containers import Container
from src.domain.entities.enums import ModelType
from src.domain.validators.dto import PaginatedResponse

TRead = TypeVar("TRead", bound=BaseModel)
TWrite = TypeVar("TWrite", bound=BaseModel)


def build_crud_router(
    *,
    prefix: str,
    tag: str,
    model_type: ModelType,
    read_dto: Type[TRead],
    write_dto: Type[TWrite],
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.get(
        "/",
        response_model=PaginatedResponse[TRead],
        status_code=status.HTTP_200_OK,
    )
    @inject
    async def list_items(
        request: Request,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, le=100),
        crud: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
    ) -> PaginatedResponse[TRead]:
        return await crud.list(
            request=request,
            model_type=model_type,
            read_dto=read_dto,
            page=page,
            page_size=page_size,
        )

    @router.get(
        "/{item_id}",
        response_model=TRead,
        status_code=status.HTTP_200_OK,
    )
    @inject
    async def retrieve_item(
        item_id: int,
        crud: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
    ) -> TRead:
        return await crud.retrieve(
            model_type=model_type,
            obj_id=item_id,
            read_dto=read_dto,
        )

    @router.post(
        "/",
        response_model=TRead,
        status_code=status.HTTP_201_CREATED,
    )
    @inject
    async def create_item(
        data: TWrite,
        crud: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
    ) -> TRead:
        return await crud.create(
            model_type=model_type,
            data=data,
            read_dto=read_dto,
        )

    @router.put(
        "/{item_id}",
        response_model=TRead,
        status_code=status.HTTP_200_OK,
    )
    @inject
    async def update_item(
        item_id: int,
        data: TWrite,
        crud: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
    ) -> TRead:
        return await crud.update(
            model_type=model_type,
            obj_id=item_id,
            data=data,
            read_dto=read_dto,
        )

    @router.delete(
        "/{item_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    @inject
    async def delete_item(
        item_id: int,
        crud: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
    ) -> None:
        await crud.delete(
            model_type=model_type,
            obj_id=item_id,
        )

    return router
