from app.api.payments_api import payments_router
from app.api.misc_api import misc_router
from app.api.companies_api import companies_router
from app.api.films_api import films_router
from app.api.user import user_router

ROUTES = {
    "/films": films_router,
    "/users": user_router
}
