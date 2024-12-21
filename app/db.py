from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_async_engine(url=settings.db.db_url, echo=True, poolclass=NullPool)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=True
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
