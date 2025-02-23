from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class ModelConfigOut(BaseModel):
    id: int
    stock_symbol: str
    input_size: int
    num_lstm_layers: int
    lstm_size: int
    dropout: float
    description: Optional[str]

class TrainingRunOut(BaseModel):
    id: int
    model_id: int
    dataset_id: int
    train_loss: Optional[float]
    val_loss: Optional[float]
    started_at: datetime
    completed_at: Optional[datetime]

class PredictionOut(BaseModel):
    date: date
    actual_price: Optional[float]
    predicted_price: float

class EvaluateModelOut(BaseModel):
    training_run_id: int
    predictions: List[PredictionOut]

class PredictModelOut(BaseModel):
    date: date
    predicted_price: float