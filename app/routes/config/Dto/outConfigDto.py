from pydantic import BaseModel

class SetConfigOut(BaseModel):
    alpha_vantage_key: str  # Masked for security (e.g., "****")
    xticks_interval: int