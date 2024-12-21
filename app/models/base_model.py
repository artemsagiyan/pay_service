from datetime import datetime
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column


class BaseModel:
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    update_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)