from fastapi import APIRouter
from app.routes.plot.plot_controller import router as plot_router

router = APIRouter(prefix="/api/plot")

router.include_router(plot_router)