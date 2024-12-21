from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from app.db import Base

user_film_association = Table(
    'user_film_association', Base.metadata,
    Column('user_id', PgUUID(as_uuid=True), ForeignKey('users.uuid'), primary_key=True),
    Column('film_id', PgUUID(as_uuid=True), ForeignKey('films.film_id'), primary_key=True)
)