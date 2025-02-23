from app.main import get_session
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.routes.model.Dto.inModelDto import TrainModelIn
from app.routes.model.Dto.outModelDto import TrainingRunOut
from app.services.model import training_service  # Placeholder

router = APIRouter()

@router.post("/train", response_model=TrainingRunOut, description="Trains an LSTM model using persisted train/validation datasets.")
def train_model(data_in: TrainModelIn, session: Session = Depends(get_session)):
    
    result = training_service.train_model(
        model_id=data_in.model_id,
        dataset_id=data_in.dataset_id,
        batch_size=data_in.batch_size,
        num_epochs=data_in.num_epochs,
        learning_rate=data_in.learning_rate,
        session=session
    )
    return TrainingRunOut(
        id=result["id"],
        model_id=result["model_id"],
        dataset_id=result["dataset_id"],
        train_loss=result["train_loss"],
        val_loss=result["val_loss"],
        started_at=result["started_at"],
        completed_at=result["completed_at"]
    )