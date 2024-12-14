from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import SqlException
from app.models.payments_model import Payment
from app.schemas.payment_schemas import PaymentSchema
from app.repositories.base_repo import BaseRepo


class PaymentRepo(BaseRepo):
    async def get_all(self, session: AsyncSession) -> list[PaymentSchema] | list:
        result = await session.execute(select(Payment))
        return [
            PaymentSchema.model_validate(payment) for payment in result.scalars().all()
        ]

    async def add(self, payment: Payment, session: AsyncSession) -> None:
        try:
            session.add(payment)
            await session.commit()
        except SQLAlchemyError as exc:
            await session.rollback()
            raise SqlException(message=str(exc))

    async def get_payment_by_payment_id(
        self, payment_id: str, session: AsyncSession
    ) -> PaymentSchema | None:
        result = await session.execute(
            select(Payment).where(Payment.payment_id == payment_id)
        )
        data = result.scalars().one_or_none()
        if not data:
            return None
        return PaymentSchema.model_validate(data)

    async def update_payment_status(
        self, payment_id: str, payment_status: str, session: AsyncSession
    ) -> None:
        try:
            await session.execute(
                update(Payment)
                .where(Payment.payment_id == payment_id)
                .values(payment_status=payment_status)
            )
            await session.commit()
        except SQLAlchemyError as exc:
            await session.rollback()
            raise SqlException(message=str(exc))


payment_repo = PaymentRepo()
