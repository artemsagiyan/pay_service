import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.base_payment_client import base_payment_client
from app.exceptions import SqlException, DuplicateException
from app.models.payments_model import Payment
from app.repositories.payment_repo import payment_repo
from app.schemas.payment_schemas import PaymentSchema
from app.enums import PaymentStatus

logger = structlog.get_logger()


class PaymentService:
    def __init__(self):
        self.repo = payment_repo

    async def get_all_payments(self, session: AsyncSession) -> list[PaymentSchema]:
        payments = await self.repo.get_all(session=session)
        return payments

    async def get_payment_by_payment_id(
        self, payment_id: str, session: AsyncSession
    ) -> PaymentSchema | None:
        payment = await self.repo.get_payment_by_payment_id(
            payment_id=payment_id, session=session
        )
        return payment

    async def create_base_payment(
        self, session: AsyncSession, payment_data: PaymentSchema
    ) -> None:
        payment = Payment(
            user_id=payment_data.user_id,
            payment_id=payment_data.payment_id,
            amount=payment_data.amount,
            email=payment_data.email,
            type=payment_data.type,
            payment_status=PaymentStatus.PENDING,
            company_id=payment_data.company_id,
        )
        try:
            await self.repo.add(payment=payment, session=session)
        except SqlException as exc:
            raise DuplicateException(message=str(exc))

        result = await base_payment_client.post_base_payment(payment_data=payment_data)

        try:
            await self.repo.update_payment_status(
                payment_id=payment_data.payment_id,
                payment_status=result.status,
                session=session,
            )
        except SqlException as exc:
            # logger.error(
            #     f"Something went wrong when updating payment status. Current status is {result.status}"
            # )
            raise DuplicateException(message=str(exc))


payment_service = PaymentService()
