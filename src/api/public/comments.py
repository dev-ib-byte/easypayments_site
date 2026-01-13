from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query, Request
from fastapi.routing import APIRouter

from src.api.dto import CommentDTO, CreateCommentDTO, PublicCommentDTO
from src.application.use_cases.common.crud import CRUDUseCase
from src.config.containers import Container
from src.domain.entities.enums import ModelType
from src.domain.validators.dto import PaginatedResponse

router = APIRouter(tags=["Comments"], prefix="/comments")


@router.get("")
@inject
async def get_comments_list(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    crud_use_case: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
) -> PaginatedResponse[PublicCommentDTO]:
    return await crud_use_case.list(
        request=request,
        model_type=ModelType.COMMENTS,
        read_dto=PublicCommentDTO,
        page_size=page_size,
        page=page,
        filters={"active": True},
    )


@router.post("", response_model=CommentDTO, status_code=201)
@inject
async def create_comment(
    data: CreateCommentDTO,
    crud_use_case: CRUDUseCase = Depends(Provide[Container.crud_use_case]),
) -> CommentDTO:
    return await crud_use_case.create(
        model_type=ModelType.COMMENTS,
        data=data,
        read_dto=CommentDTO,
    )
