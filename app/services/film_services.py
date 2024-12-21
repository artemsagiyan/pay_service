# from mypy.types import names
import json
from asyncio import StreamReader
from typing import List, Any
from urllib.parse import urljoin
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


from app.exceptions import SqlException, DuplicateException
from app.models.companies_model import Company
from app.models.films_model import Film
from app.models.users_model import User
from app.repositories.film_repo import film_repo
# from app.repositories.company_repo import company_repo
from app.schemas.company_schemas import CompanySchema
from app.schemas.film_schemas import FilmSchema

from sqlalchemy import select

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

    async def add_film(self, film_id: int, user_id: str, session: AsyncSession) -> None:
        result = await session.execute(
            select(User).options(joinedload(User.films)).filter(User.uuid == user_id)
        )
        user_db = result.scalars().first()

        if not user_db:
            raise ValueError(f"User with id {user_id} not found.")

        try:
            film_uuid = UUID(int=film_id)
        except:
            raise ValueError(f"Incorrect film id: {film_id}")

        try:
            film = await self.get_film_info_by_film_id(film_id)
        except:
            raise ValueError(f"Do not exist film id: {film_id}")

        try:
            film_name = film['nameRu']
        except:
            raise ValueError(f"Incorrect film name: film_id: {film_id}")

        try:
            stmt = select(User).options(selectinload(User.films)).filter(User.uuid == user_id)
            result = await session.execute(stmt)
            user_db = result.scalars().first()

            if not user_db:
                raise ValueError(f"User with id {user_id} not found.")

            film_uuid = UUID(int=film_id)

            flms_find = next((film for film in user_db.films if film.film_id == film_uuid), None)

            stmt = select(Film).filter(Film.film_id == film_uuid)
            result = await session.execute(stmt)
            flm = result.scalars().first()

            if not flm:
                film_db = Film(film_id=film_uuid, name=film_name)
            else:
                film_db = flm
            if film_db not in user_db.films:
                user_db.films.append(film_db)
        except:
            pass

        await session.commit()

    async def get_favourite_films(self, user_id: str, session: AsyncSession) -> List[str]:
        stmt = select(User).options(selectinload(User.films)).filter(User.uuid == user_id)
        result = await session.execute(stmt)
        user_db = result.scalars().first()

        if not user_db:
            raise ValueError(f"User with id {user_id} not found.")

        return [film.name for film in user_db.films]

    async def delete_film_from_favourites(self, user_id: str, film_id: int, session: AsyncSession) -> List[str]:
        stmt = select(User).options(selectinload(User.films)).filter(User.uuid == user_id)
        result = await session.execute(stmt)
        user_db = result.scalars().first()

        if not user_db:
            raise ValueError(f"User with id {user_id} not found.")

        film_uuid = UUID(int=film_id)

        film_to_remove = next((film for film in user_db.films if film.film_id == film_uuid), None)

        if not film_to_remove:
            raise ValueError(f"Film with UUID {film_uuid} not found in user's favourites.")

        user_db.films.remove(film_to_remove)

        await session.commit()

        return [film.name for film in user_db.films if film.film_id != film_uuid]


film_services = FilmService()
