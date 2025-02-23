from pydantic import BaseModel
from typing import List
from datetime import date

class DataPointOut(BaseModel):
    date: date
    adjusted_close: float

class AcquireDataOut(BaseModel):
    symbol: str
    data_points: List[DataPointOut]
    num_data_points: int
    date_range: str