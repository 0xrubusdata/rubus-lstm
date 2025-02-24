from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Dataset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_id: int = Field(foreign_key="stock.id", index=True)
    window_size: int = Field(ge=1)
    train_split_size: float = Field(gt=0.0, lt=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scaler_mu: Optional[float] = None
    scaler_sd: Optional[float] = None
    train_dataset_path: Optional[str] = None
    val_dataset_path: Optional[str] = None

    stock: "Stock" = Relationship(back_populates="datasets")
    normalized_data: List["NormalizedData"] = Relationship(back_populates="dataset")
    training_runs: List["TrainingRun"] = Relationship(back_populates="dataset")