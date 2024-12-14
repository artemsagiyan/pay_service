from fastapi import APIRouter, Depends
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_409_CONFLICT
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.payment_schemas import PaymentSchema
from app.services.payment_service import payment_service
from app.db import get_session
from app.exceptions import DuplicateException

payments_router = APIRouter(tags=["payments"])


@payments_router.get("", response_model=list[PaymentSchema] | None)
async def get_payments(session: AsyncSession = Depends(get_session)):
    all_payments = await payment_service.get_all_payments(session=session)
    if not all_payments:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return all_payments


@payments_router.get("/{payment_id}", response_model=PaymentSchema | None)
async def get_payment_by_id(
    payment_id: str, session: AsyncSession = Depends(get_session)
):
    payment = await payment_service.get_payment_by_payment_id(
        payment_id=payment_id, session=session
    )
    if not payment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return payment


@payments_router.post("/base")
async def create_payment(
    payment_data: PaymentSchema, session: AsyncSession = Depends(get_session)
):
    try:
        await payment_service.create_base_payment(
            session=session, payment_data=payment_data
        )
    except DuplicateException:
        return Response(status_code=HTTP_409_CONFLICT)
    return Response(status_code=HTTP_201_CREATED)


# @payments_router.post("/sbp")
# async def create_sbp_payment():
#     return "OK"
