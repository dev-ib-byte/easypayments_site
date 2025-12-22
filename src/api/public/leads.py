from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.routing import APIRouter

from src.api.dto import LeadMagnitDTO, NewsletterDTO
from src.application.use_cases.leads.submit_leadmagnit import LeadMagnitSubmitUseCase
from src.application.use_cases.leads.submit_leadmagnit_company import LeadMagnitCompanySubmitUseCase
from src.application.use_cases.leads.submit_newsletter import NewsletterSubmitUseCase
from src.config.containers import Container

router = APIRouter(tags=["Leads"], prefix="/leads")


@router.post("/leadmagnit")
@inject
async def submit_leadmagnit(
    data: LeadMagnitDTO,
    use_case: LeadMagnitSubmitUseCase = Depends(Provide[Container.leadmagnit_submit_use_case]),
):
    await use_case.execute(data)
    return {"status": "ok"}


@router.post("/leadmagnit/company")
@inject
async def submit_leadmagnit_company(
    data: LeadMagnitDTO,
    use_case: LeadMagnitCompanySubmitUseCase = Depends(
        Provide[Container.leadmagnit_company_submit_use_case]
    ),
):
    await use_case.execute(data)
    return {"status": "ok"}


@router.post("/newsletter")
@inject
async def submit_newsletter(
    data: NewsletterDTO,
    use_case: NewsletterSubmitUseCase = Depends(Provide[Container.newsletter_submit_use_case]),
):
    await use_case.execute(data)
    return {"status": "ok"}
