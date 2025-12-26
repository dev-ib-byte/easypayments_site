from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Path, Query, Request
from fastapi.routing import APIRouter
from starlette import status

from src.api.dto import (
    CreateTelegramPushDTO,
    TelegramPushDTO,
    UpdateTelegramPushDTO,
)
from src.application.use_cases.common.crud import CRUDUseCase
from src.config.containers import Container
from src.domain.entities.enums import ModelType
from src.domain.validators.dto import PaginatedResponse

router = APIRouter(tags=["Telegram Push"], prefix="/telegram-push")


@router.get("", response_model=PaginatedResponse[TelegramPushDTO])
@inject
async def get_push_list(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    crud_use_case: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
) -> PaginatedResponse[TelegramPushDTO]:
    return await crud_use_case.list(
        request=request,
        model_type=ModelType.TELEGRAM_PUSH_USERS,
        read_dto=TelegramPushDTO,
        page_size=page_size,
        page=page,
    )


@router.get("/{push_id}", response_model=TelegramPushDTO)
@inject
async def get_push_by_id(
    request: Request,
    push_id: int = Path(..., ge=1),
    crud_use_case: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
):
    return await crud_use_case.retrieve(
        model_type=ModelType.TELEGRAM_PUSH_USERS,
        obj_id=push_id,
        read_dto=TelegramPushDTO,
    )


@router.post("", response_model=TelegramPushDTO, status_code=201)
@inject
async def create_push(
    request: Request,
    data: CreateTelegramPushDTO,
    crud_use_case: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
):
    return await crud_use_case.create(
        model_type=ModelType.TELEGRAM_PUSH_USERS,
        data=data,
        read_dto=TelegramPushDTO,
    )


@router.patch("/{push_id}", response_model=TelegramPushDTO)
@inject
async def update_push(
    request: Request,
    push_id: int = Path(..., ge=1),
    data: UpdateTelegramPushDTO = ...,
    crud_use_case: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
):
    return await crud_use_case.update(
        model_type=ModelType.TELEGRAM_PUSH_USERS,
        obj_id=push_id,
        data=data,
        read_dto=TelegramPushDTO,
    )


@router.delete("/{push_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_push(
    request: Request,
    push_id: int = Path(..., ge=1),
    crud_use_case: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
):
    await crud_use_case.delete(
        model_type=ModelType.TELEGRAM_PUSH_USERS,
        obj_id=push_id,
    )
