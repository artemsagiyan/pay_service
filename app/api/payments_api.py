from fastapi import APIRouter

payments_router = APIRouter(tags=["payments"])


@payments_router.get("/")
async def get_payments():
    return "OK"


@payments_router.post("/")
async def create_payments():
    return "OK"
