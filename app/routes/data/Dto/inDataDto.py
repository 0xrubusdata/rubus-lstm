from pydantic import BaseModel
from typing import Optional

class AcquireDataIn(BaseModel):
    symbol: str  # e.g., "IBM"
    outputsize: Optional[str] = "full"  # "compact" or "full"