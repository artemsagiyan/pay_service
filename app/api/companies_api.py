from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks
from app.db import get_session
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.company_service import company_service
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND

companies_router = APIRouter(tags=["companies"])


@companies_router.get("", response_model=list| None)
async def get_all_companies(session: AsyncSession = Depends(get_session)):
    all_companies = await company_service.get_all_companies(session=session)
    if not all_companies:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return all_companies


@companies_router.post("")
async def create_company():
    return "OK"
