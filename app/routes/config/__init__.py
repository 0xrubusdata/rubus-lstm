from fastapi import APIRouter
from app.routes.config.config_controller import router as config_router

router = APIRouter(prefix="/api")

router.include_router(config_router)