from uuid import UUID, uuid4
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base
from app.security.auth import pwd_context


class User(Base):
    __tablename__ = 'users'

    uuid = Column(UUID, primary_key=True, unique=True, default=uuid4)
    username = Column(String(256), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    films = relationship("Film", secondary="user_film_association", back_populates="users")

    def __repr__(self):
        return f"User(uuid={self.uuid}, username={self.username}, films={self.films})"

    def __str__(self):
        return f"User(uuid={self.uuid}, username={self.username}, films={self.films})"

    # Метод для хэширования пароля
    def set_password(self, password: str):
        self.password = pwd_context.hash(password)

    # Метод для проверки пароля
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)