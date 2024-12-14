from sqlalchemy.ext.asyncio import AsyncSession

from app.models.companies_model import Company
from app.repositories.company_repo import company_repo
from app.schemas.company_schemas import CompanySchema


class CompanyService:

    def __init__(self):
        self.repo = company_repo


    async def get_all_companies(self, session: AsyncSession) -> list[CompanySchema]:
        companies = await self.repo.get_all(session=session)
        return companies


company_service = CompanyService()