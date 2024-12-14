from sqlalchemy import Column, Numeric, String, UUID, ForeignKey, Integer
from app.db import Base
from app.models.base_model import BaseModel


class Payment(BaseModel, Base):
    __tablename__ = "payments"

    user_id = Column(String, nullable=False)
    payment_id = Column(String, nullable=False, unique=True)
    amount = Column(Numeric(10, 2), nullable=False)
    email = Column(String)
    type = Column(String(30), nullable=False)
    payment_status = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)

    def __repr__(self):
        return (
            f"Payment(user_id={self.user_id!r}, "
            f"payment_id={self.payment_id!r}, "
            f"amount={self.amount!r}, "
            f"email={self.email!r}, "
            f"type={self.type!r}, "
            f"payment_status={self.payment_status!r}, "
        )

    def __str__(self):
        return (
            f"Payment(user_id={self.user_id!r}, "
            f"payment_id={self.payment_id!r}, "
            f"amount={self.amount!r}, "
            f"email={self.email!r}, "
            f"type={self.type!r}, "
            f"payment_status={self.payment_status!r}, "
        )
