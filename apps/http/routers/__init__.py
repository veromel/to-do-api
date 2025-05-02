from fastapi import APIRouter

from apps.http.routers.users_router import users_router
from apps.http.routers.tasks_router import tasks_router
from apps.http.routers.auth_router import auth_router

router = APIRouter()
router.include_router(
    users_router,
    prefix="/api",
    tags=["Users"],
)
router.include_router(
    tasks_router,
    prefix="/api",
    tags=["Tasks"],
)
router.include_router(auth_router, prefix="/api", tags=["Auth"])
