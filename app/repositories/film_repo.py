from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import SqlException
from app.models.companies_model import Company
from app.models.films_model import Film
from app.repositories.base_repo import BaseRepo
# from app.schemas.company_schemas import CompanySchema
from app.schemas.film_schemas import FilmSchema


class FilmRepo(BaseRepo):
    async def get_all(self, session: AsyncSession) -> list[FilmSchema]:
        result = await session.execute(select(Film))
        return [
            FilmSchema.model_validate(film) for film in result.scalars().all()
        ]

    async def add(self, film: Film, session: AsyncSession) -> None:
        try:
            session.add(film)
            await session.commit()
        except SQLAlchemyError as exc:
            await session.rollback()
            raise SqlException(message=str(exc))


film_repo = FilmRepo()
