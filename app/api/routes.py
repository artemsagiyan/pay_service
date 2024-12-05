from app.api.payments_api import payments_router
from app.api.misc_api import misc_router
from app.api.companies_api import companies_router


ROUTES = {
    "": misc_router,
    "/companies": companies_router,
    "/payments": payments_router,
}
