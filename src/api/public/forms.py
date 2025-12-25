from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.routing import APIRouter
from starlette.requests import Request

from src.api.dto import FormOrderDTO, FormSubmitDTO
from src.application.use_cases.forms.submit_form import SubmitFormUseCase
from src.config.containers import Container

router = APIRouter(tags=["Forms"], prefix="/forms")


@router.post("", response_model=FormOrderDTO)
@inject
async def submit_form(
    request: Request,
    data: FormSubmitDTO,
    use_case: SubmitFormUseCase = Depends(Provide[Container.submit_form_use_case]),
) -> FormOrderDTO:
    client_ip = request.client.host if request.client else None
    result = await use_case.execute(data, client_ip=client_ip)
    return FormOrderDTO.model_validate(result)
