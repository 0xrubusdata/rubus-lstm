from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.config.database import get_session    
from app.models import Stock, ModelConfig
from app.routes.model.Dto.inModelDto import EvaluateModelIn
from app.routes.model.Dto.outModelDto import EvaluateModelOut
 
from app.services.model import evaluation_service  # Placeholder


router = APIRouter()

@router.post("/evaluate", response_model=EvaluateModelOut, description="Evaluates a trained model by comparing predictions to actual prices.")
def evaluate_model(data_in: EvaluateModelIn, session: Session = Depends(get_session)):
    
    result = evaluation_service.evaluate_model(
        training_run_id=data_in.training_run_id,
        session=session
    )
    return EvaluateModelOut(
        training_run_id=data_in.training_run_id,
        predictions=[
            {"date": p["date"], "actual_price": p["actual_price"], "predicted_price": p["predicted_price"]}
            for p in result["predictions"]
        ]
    )

@router.get("/evaluate/{model_id}", response_model=EvaluateModelOut, description="Evaluates a trained model by comparing predictions to actual prices.")
def evaluate_model(data_in: EvaluateModelIn, session: Session = Depends(get_session)):
    
    result = evaluation_service.evaluate_model(
        training_run_id=data_in.training_run_id,
        session=session
    )
    return EvaluateModelOut(
        training_run_id=data_in.training_run_id,
        predictions=[
            {"date": p["date"], "actual_price": p["actual_price"], "predicted_price": p["predicted_price"]}
            for p in result["predictions"]
        ]
    )