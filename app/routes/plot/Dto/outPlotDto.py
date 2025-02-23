from pydantic import BaseModel

class PlotPricesOut(BaseModel):
    image_base64: str  # Base64-encoded PNG image