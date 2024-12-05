from sqlalchemy import Column, Integer, String
from app.db import Base
from app.models.base_model import BaseModel


class Company(Base):
    __tablename__ = "companies"

    name = Column(String)
    company_id = Column(Integer, primary_key=True, autoincrement=True)
