from app.main import get_session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.routes.plot.Dto.inPlotDto import PlotPricesIn
from app.routes.plot.Dto.outPlotDto import PlotPricesOut
from app.services.plot import serve_plots_service

router = APIRouter()

@router.post("/prices", response_model=PlotPricesOut, description="Generates a plot (e.g., actual vs. predicted) as a base64-encoded PNG image.")
def serve_prices_plot(data_in: PlotPricesIn, session: Session = Depends(get_session)):

    image_base64 = serve_plots_service.plot_prices(
        training_run_id=data_in.training_run_id,
        plot_type=data_in.plot_type,
        session=session
    )
    return PlotPricesOut(image_base64=image_base64)