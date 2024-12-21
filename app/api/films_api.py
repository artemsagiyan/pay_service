import json

from fastapi import APIRouter, Depends
from starlette.responses import Response
from starlette.status import *
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_model import BaseModel
from app.schemas.film_schemas import FilmSchema
from app.schemas.payment_schemas import PaymentSchema
from app.services.film_services import film_services
# from app.services.payment_service import payment_service
from app.db import get_session
from app.exceptions import DuplicateException

from pydantic import BaseModel, Field
from typing import Optional

films_router = APIRouter(tags=["films"])

class FilmSearchQuery(BaseModel):
    film_name: Optional[str] = Field(None, description="Название фильма")

@films_router.get("/search", response_model=list[PaymentSchema] | None)
async def get_films(session: AsyncSession = Depends(get_session, ), query: FilmSearchQuery = Depends(),):
    if not query.film_name:
        Response(status_code=HTTP_400_BAD_REQUEST, content="Empty film name")

    films_by_name = await film_services.get_films_by_name(query.film_name)

    return Response(status_code=HTTP_200_OK, content=json.dumps(films_by_name, ensure_ascii=False, indent=4))

@films_router.get("/{film_id}", response_model=list[FilmSchema] | None)
async def get_film_info_by_film_id(film_id: int, session: AsyncSession = Depends(get_session, )):

    film_info = await film_services.get_film_info_by_film_id(film_id)

    return Response(status_code=HTTP_200_OK, content=json.dumps(film_info, ensure_ascii=False, indent=4))

@films_router.get("favourites/{film_id}", response_model=list[FilmSchema] | None)
async def add_film_to_favourites(film_id: int, session: AsyncSession = Depends(get_session, )):

    film_info = await film_services.add_film(film_id)

    return Response(status_code=HTTP_200_OK, content=json.dumps(film_info, ensure_ascii=False, indent=4))
