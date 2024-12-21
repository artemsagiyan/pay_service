from uuid import UUID, uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import relationship

from app.db import Base


class Film(Base):
    __tablename__ = 'films'

    film_id = Column(PgUUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    name = Column(String(256), nullable=False)

    users = relationship("User", secondary="user_film_association", back_populates="films")

    def __repr__(self):
        return f"Film(film_id={self.film_id}, name={self.name})"

    def __str__(self):
        return f"Film(film_id={self.film_id}, name={self.name})"