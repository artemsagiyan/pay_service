from uuid import UUID, uuid4
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as U_UUID

from app.db import Base
from app.models.base_model import BaseModel


class Film(BaseModel, Base):
    __tablename__ = 'films'

    film_id: Mapped[UUID] = mapped_column(U_UUID(as_uuid=True), default=uuid4, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(256))