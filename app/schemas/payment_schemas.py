from decimal import Decimal
from pydantic import BaseModel
from app.enums import PaymentStatus


class PaymentSchema(BaseModel):
    user_id: str
    payment_id: str
    amount: Decimal
    email: str | None
    type: str | None
    payment_status: str | None
    company_id: int

    class Config:
        from_attributes = True


class PaymentResultSchema(BaseModel):
    status: PaymentStatus
    payment_id: str


# example = PaymentSchema(
#     user_id="uuid",
#     payment_id= "payment_id",
#     amount=Decimal("10.00"),
#     email="email",
#     type="type",
#     payment_status="payment_status",
#     company_id=1,
# )
#
# print(example)
