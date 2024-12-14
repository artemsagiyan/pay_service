from fastapi import APIRouter, Depends
from requests import session
from app.db import get_session
from app.exceptions import DuplicateException
from app.schemas.company_schemas import CompanySchema
from app.services.company_service import company_service
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_201_CREATED
from sqlalchemy.ext.asyncio import AsyncSession

companies_router = APIRouter(tags=["companies"])


@companies_router.get("", response_model=list[CompanySchema] | None)
async def get_all_companies(session: AsyncSession = Depends(get_session)):
    all_companies = await company_service.get_all_companies(session=session)
    if not all_companies:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return all_companies


@companies_router.post("", response_model=None)
async def create_company(
    request: CompanySchema,
    session: AsyncSession = Depends(get_session),
):
    try:
        await company_service.add_company(request=request, session=session)
    except DuplicateException:
        return Response(status_code=HTTP_409_CONFLICT)
    return Response(status_code=HTTP_201_CREATED)
