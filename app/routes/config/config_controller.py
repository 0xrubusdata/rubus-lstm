from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config.database import get_session
from app.routes.config.Dto.inConfigDto import SetConfigIn
from app.routes.config.Dto.outConfigDto import GetConfigOut, SetConfigOut
from app.services.config import config_service


router = APIRouter()

@router.post("/config", response_model=SetConfigOut, description="Sets the Alpha Vantage API key and plot xticks interval.")
async def set_config(data_in: SetConfigIn, session: Session = Depends(get_session)):

    config_service.set_config(
        alpha_vantage_key=data_in.alpha_vantage_key,
        xticks_interval=data_in.xticks_interval,
        session=session
    )
    return SetConfigOut(
        alpha_vantage_key=data_in.alpha_vantage_key[-4:].rjust(len(data_in.alpha_vantage_key), "*"),  # Mask key
        xticks_interval=data_in.xticks_interval
    )

@router.get("/config", response_model=GetConfigOut, description="Get the Alpha Vantage API key and plot xticks interval.")
async def get_config(session: Session = Depends(get_session)):

    result = config_service.get_config(
        session=session
    )
    return SetConfigOut(
        alpha_vantage_key=result.alpha_vantage_key[-4:].rjust(len(result.alpha_vantage_key), "*"),  # Mask key
        xticks_interval=result.xticks_interval
    )