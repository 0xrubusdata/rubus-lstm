from app.main import get_session
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.routes.model.Dto.inModelDto import PredictModelIn
from app.routes.model.Dto.outModelDto import PredictModelOut
from app.services.model import prediction_service  # Placeholder

router = APIRouter()

@router.post("/predict", response_model=PredictModelOut, description="Predicts the next day's stock price using a trained model.")
def predict_model(data_in: PredictModelIn, session: Session = Depends(get_session)):

    result = prediction_service.predict_next_day(
        training_run_id=data_in.training_run_id,
        session=session
    )
    return PredictModelOut(
        date=result["date"],
        predicted_price=result["predicted_price"]
    )