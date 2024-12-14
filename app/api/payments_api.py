from fastapi import APIRouter

payments_router = APIRouter(tags=["payments"])


@payments_router.get("")
async def get_payments():
    return "OK"


@payments_router.get("/{payment_id}")
async def get_payments_by_id():
    return "OK"


@payments_router.post("/base")
async def create_payments():
    return "OK"


@payments_router.post("/sbp")
async def create_sbp_payment():
    return "OK"
