from app.main import get_session
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.routes.config.Dto.inConfigDto import SetConfigIn
from app.routes.config.Dto.outConfigDto import SetConfigOut
from app.services.config import config_service

router = APIRouter()

@router.post("/set", response_model=SetConfigOut, description="Sets the Alpha Vantage API key and plot xticks interval.")
def set_config(data_in: SetConfigIn, session: Session = Depends(get_session)):

    config_service.set_config(
        alpha_vantage_key=data_in.alpha_vantage_key,
        xticks_interval=data_in.xticks_interval,
        session=session
    )
    return SetConfigOut(
        alpha_vantage_key=data_in.alpha_vantage_key[-4:].rjust(len(data_in.alpha_vantage_key), "*"),  # Mask key
        xticks_interval=data_in.xticks_interval
    )