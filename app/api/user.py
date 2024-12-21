# app/routers/user.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.models.users_model import User
from app.schemas.user_schemas import UserCreate, Token
from app.security.auth import hash_password, create_access_token, verify_password
from app.security.auth import oauth2_scheme

user_router = APIRouter(tags=["users"])


@user_router.post("/register", response_model=Token)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Проверка на существующего пользователя
    stmt = select(User).filter(User.username == user.username)
    result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    # Создание нового пользователя
    new_user = User(username=user.username)
    new_user.set_password(user.password)
    session.add(new_user)
    await session.commit()

    # Генерация JWT токена
    token_data = {"user_id": str(new_user.uuid), "username": new_user.username}
    access_token = await create_access_token(data=token_data)

    return Token(access_token=access_token, token_type="bearer")


@user_router.post("/login", response_model=Token)
async def login(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Поиск пользователя
    stmt = select(User).filter(User.username == user.username)
    result = await session.execute(stmt)
    db_user = result.scalar_one_or_none()

    if db_user is None or not db_user.verify_password(user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Генерация JWT токена
    token_data = {"user_id": str(db_user.uuid), "username": db_user.username}
    access_token = await create_access_token(data=token_data)

    return Token(access_token=access_token, token_type="bearer")
