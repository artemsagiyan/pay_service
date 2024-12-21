# from mypy.types import names
import json
from asyncio import StreamReader
from typing import List, Any
from urllib.parse import urljoin

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import SqlException, DuplicateException
from app.models.companies_model import Company
from app.models.films_model import Film
from app.repositories.film_repo import film_repo
# from app.repositories.company_repo import company_repo
from app.schemas.company_schemas import CompanySchema
from app.schemas.film_schemas import FilmSchema

from app.config import settings

import aiohttp


class FilmService:
    def __init__(self):
        self.repo = film_repo

    async def get_films_by_name(self, name: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=urljoin(settings.kinopoisk.api_url,
                                "api/v2.1/films/search-by-keyword?keyword={}".format(name)
                                ),
                    headers={"X-API-KEY": settings.kinopoisk.api_key},
            ) as response:
                films = json.loads(await response.text())

        return films['films']

    async def get_film_info_by_film_id(self, film_id) -> Any:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=urljoin(settings.kinopoisk.api_url,
                                "api/v2.2/films/{}".format(film_id)
                                ),
                    headers={"X-API-KEY": settings.kinopoisk.api_key},
            ) as response:
                film_info = json.loads(await response.text())

        return film_info

    async def add_film(self, request: FilmSchema, session: AsyncSession) -> None:
        film = Film(name=request.name, film_id=request.film_id)
        try:
            await self.repo.add(film=film, session=session)
        except SqlException as exc:
            raise DuplicateException(message=str(exc))




film_services = FilmService()
