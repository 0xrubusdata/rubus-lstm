from pydantic import BaseModel
from typing import Literal

class PlotPricesIn(BaseModel):
    training_run_id: int
    plot_type: Literal["actual_vs_predicted", "train_vs_val", "zoom_val", "next_day"]  # Supported plot types