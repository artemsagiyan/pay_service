# app/schemas/user.py
from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: UUID
    username: str
