from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class ModelConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_id: int = Field(foreign_key="stock.id", index=True)
    model_name: str = Field(default=None, max_length=50)
    input_size: int = Field(default=1, ge=1)
    num_lstm_layers: int = Field(default=2, ge=1)
    lstm_size: int = Field(default=32, ge=1)
    dropout: float = Field(default=0.2, ge=0.0, le=1.0)
    description: Optional[str] = Field(default=None, max_length=255)

    stock: "Stock" = Relationship(back_populates="model_configs")
    training_runs: List["TrainingRun"] = Relationship(back_populates="model_config")
    