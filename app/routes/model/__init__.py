from fastapi import APIRouter
from app.routes.model.define_controller import router as define_router
from app.routes.model.evaluate_controller import router as evaluate_router
from app.routes.model.train_controller import router as train_router
from app.routes.model.predict_controller import router as predict_router

router = APIRouter(prefix="/api/model")

router.include_router(define_router)
router.include_router(evaluate_router)
router.include_router(train_router)
router.include_router(predict_router)