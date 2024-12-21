from asyncpg.pgproto.pgproto import UUID
from pydantic import BaseModel


class FilmSchema(BaseModel):
    film_id: UUID
    name: str

    class Config:
        from_attributes = True
