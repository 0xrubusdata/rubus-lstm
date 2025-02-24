from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.config.database import get_session
from app.routes.data.Dto.inDataDto import AcquireDataIn, AcquireDataSourceSymbol 
from app.routes.data.Dto.outDataDto import AcquireDataOut
from app.services.data import acquisition_service  # Placeholder

router = APIRouter()

@router.get("/acquire", response_model=AcquireDataOut, description="Fetches stock data from Alpha Vantage and persists it for training.")
async def all_acquired_data(session: Session = Depends(get_session)):
    result = acquisition_service.get_acquired_all_data(
        session=session
    )
    return AcquireDataOut(
        symbol=result["symbol"],
        data_points=[{"date": dp.date, "adjusted_close": dp.adjusted_close} for dp in result["data_points"]],
        num_data_points=result["num_data_points"],
        date_range=result["date_range"]
    )

@router.get("/acquire/source/{source_id}", response_model=AcquireDataOut, description="Fetches stock data from Alpha Vantage and persists it for training.")
async def all_acquired_data_by_source(data_in: AcquireDataIn, session: Session = Depends(get_session)):
    result = acquisition_service.acquire_data(
        symbol=data_in.symbol,
        data_source=data_in.data_source, 
        outputsize=data_in.outputsize,
        session=session
    )
    return AcquireDataOut(
        symbol=result["symbol"],
        data_points=[{"date": dp.date, "adjusted_close": dp.adjusted_close} for dp in result["data_points"]],
        num_data_points=result["num_data_points"],
        date_range=result["date_range"]
    )

@router.get("/acquire/symbol/{symbol_id}", response_model=AcquireDataOut, description="Fetches stock data from Alpha Vantage and persists it for training.")
async def all_acquired_data_by_symbol(data_in: AcquireDataIn, session: Session = Depends(get_session)):
    result = acquisition_service.acquire_data(
        symbol=data_in.symbol,
        data_source=data_in.data_source, 
        outputsize=data_in.outputsize,
        session=session
    )
    return AcquireDataOut(
        symbol=result["symbol"],
        data_points=[{"date": dp.date, "adjusted_close": dp.adjusted_close} for dp in result["data_points"]],
        num_data_points=result["num_data_points"],
        date_range=result["date_range"]
    )

@router.get("/acquire/source/{source_id}/symbol/{symbol_id}", response_model=AcquireDataOut, description="Fetches stock data from Alpha Vantage and persists it for training.")
async def all_acquired_data_by_source_and_symbol(data_in: AcquireDataIn, session: Session = Depends(get_session)):
    result = acquisition_service.acquire_data(
        symbol=data_in.symbol,
        data_source=data_in.data_source, 
        outputsize=data_in.outputsize,
        session=session
    )
    return AcquireDataOut(
        symbol=result["symbol"],
        data_points=[{"date": dp.date, "adjusted_close": dp.adjusted_close} for dp in result["data_points"]],
        num_data_points=result["num_data_points"],
        date_range=result["date_range"]
    )

@router.post("/acquire", response_model=AcquireDataOut, description="Fetches stock data from Alpha Vantage and persists it for training.")
async def acquire_data(data_in: AcquireDataIn, session: Session = Depends(get_session)):
    result = acquisition_service.acquire_data(
        symbol=data_in.symbol,
        data_source=data_in.data_source, 
        outputsize=data_in.outputsize,
        session=session
    )
    return AcquireDataOut(
        symbol=result["symbol"],
        data_points=[{"date": dp.date, "adjusted_close": dp.adjusted_close} for dp in result["data_points"]],
        num_data_points=result["num_data_points"],
        date_range=result["date_range"]
    )