from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class TrainingRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config_id: int = Field(foreign_key="modelconfig.id", index=True)
    dataset_id: int = Field(foreign_key="dataset.id", index=True)
    batch_size: int = Field(ge=1)
    num_epochs: int = Field(ge=1)
    learning_rate: float = Field(gt=0.0)
    train_loss: Optional[float] = None
    val_loss: Optional[float] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    model_state_path: Optional[str] = Field(default=None, max_length=255)

    # Use string literals for relationships
    model_config: "ModelConfig" = Relationship(back_populates="training_runs")
    dataset: "Dataset" = Relationship(back_populates="training_runs")
    predictions: List["Prediction"] = Relationship(back_populates="training_run")

    