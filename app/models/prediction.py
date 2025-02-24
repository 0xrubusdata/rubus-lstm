from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    training_run_id: int = Field(foreign_key="trainingrun.id", index=True)
    date: datetime = Field(index=True)
    actual_price: Optional[float] = None
    predicted_price: float

    training_run: "TrainingRun" = Relationship(back_populates="predictions")