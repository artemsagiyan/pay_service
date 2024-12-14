import asyncio

from app.schemas.payment_schemas import PaymentSchema, PaymentResultSchema
from app.enums import PaymentStatus


class BasePaymentClient:
    async def post_base_payment(
        self, payment_data: PaymentSchema
    ) -> PaymentResultSchema:
        await asyncio.sleep(5)
        return PaymentResultSchema(
            status=PaymentStatus.COMPLETED, payment_id=payment_data.payment_id
        )


base_payment_client = BasePaymentClient()
