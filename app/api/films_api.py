import json
from http.client import HTTPException

from fastapi import APIRouter, Depends
from starlette.responses import Response
from starlette.status import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.base_model import BaseModel
from app.models.users_model import User
from app.schemas.film_schemas import FilmSchema
from app.schemas.payment_schemas import PaymentSchema
from app.security.auth import get_user_id_from_token, get_current_user
from app.services.film_services import film_services
# from app.services.payment_service import payment_service
from app.db import get_session
from app.exceptions import DuplicateException

from pydantic import BaseModel, Field
from typing import Optional, List

films_router = APIRouter(tags=["films"])

class FilmSearchQuery(BaseModel):
    film_name: Optional[str] = Field(None, description="Название фильма")

@films_router.get("/search", response_model=list[PaymentSchema] | None)
async def get_films(session: AsyncSession = Depends(get_session, ), query: FilmSearchQuery = Depends(), user_id: str = Depends(get_user_id_from_token)):
    if not query.film_name:
        Response(status_code=HTTP_400_BAD_REQUEST, content="Empty film name")

    films_by_name = await film_services.get_films_by_name(query.film_name)

    return Response(status_code=HTTP_200_OK, content=json.dumps(films_by_name, ensure_ascii=False, indent=4))

@films_router.get("/{film_id}", response_model=list[FilmSchema] | None)
async def get_film_info_by_film_id(film_id: int, session: AsyncSession = Depends(get_session, ), user_id: str = Depends(get_user_id_from_token)):

    film_info = await film_services.get_film_info_by_film_id(film_id)

    return Response(status_code=HTTP_200_OK, content=json.dumps(film_info, ensure_ascii=False, indent=4))

@films_router.post("/favourites/{film_id}", response_model=list[FilmSchema] | None)
async def add_film_to_favourites(
    film_id: int,
    session: AsyncSession = Depends(get_session),
    user_id: str = Depends(get_user_id_from_token)
):
    try:
        film_info = await film_services.add_film(film_id, user_id, session)
    except Exception as error:
        return Response(status_code=HTTP_400_BAD_REQUEST, content=str(error))

    return Response(status_code=201, content=json.dumps({"message": "Film has been added to favourites"}, ensure_ascii=False, indent=4))

@films_router.get("/favourites/films", response_model=List[str])
async def get_favourite_films(user_id: str = Depends(get_user_id_from_token), session: AsyncSession = Depends(get_session)):

    try:
        favourite_films = await film_services.get_favourite_films(user_id, session)
    except Exception as error:
        return Response(status_code=HTTP_400_BAD_REQUEST, content=str(error))
    return Response(status_code=HTTP_200_OK, content=json.dumps(favourite_films, ensure_ascii=False, indent=4))

@films_router.delete("/favourites/{film_id}", response_model=list[FilmSchema] | None)
async def delete_film_from_favourites(film_id: int, session: AsyncSession = Depends(get_session, ), user_id: str = Depends(get_user_id_from_token)):

    try:
        film_info = await film_services.delete_film_from_favourites(user_id, film_id, session)
    except Exception as error:
        return Response(status_code=HTTP_400_BAD_REQUEST, content=str(error))
    return Response(status_code=HTTP_204_NO_CONTENT)