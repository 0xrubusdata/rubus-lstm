from pydantic import BaseModel

class SetConfigIn(BaseModel):
    alpha_vantage_key: str
    xticks_interval: int = 90