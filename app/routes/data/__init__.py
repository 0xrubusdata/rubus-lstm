from fastapi import APIRouter
from app.routes.data.acquire_controller import router as acquire_router
from app.routes.data.prepare_controller import router as prepare_router

router = APIRouter(prefix="/api/data")

router.include_router(acquire_router)
router.include_router(prepare_router)