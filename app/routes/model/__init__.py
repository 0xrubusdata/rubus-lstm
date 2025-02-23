from .defineAction import router as define_router
from .trainAction import router as train_router
from .evaluateAction import router as evaluate_router
from .predictAction import router as predict_router

router = define_router
router.include_router(train_router)
router.include_router(evaluate_router)
router.include_router(predict_router)

__all__ = ["router"]