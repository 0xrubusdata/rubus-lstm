from sqlmodel import Session, select
from app.models import Stock, DataPoint
from app.config.settings import CONFIG
from alpha_vantage.timeseries import TimeSeries
from .normalizationService import normalize_data
from .datasetprepService import prepare_dataset

class AcquisitionService:
    @staticmethod
    def acquire_data(symbol: str, outputsize: str, session: Session):
        stock = session.exec(select(Stock).where(Stock.symbol == symbol)).first()
        if not stock:
            stock = Stock(symbol=symbol)
            session.add(stock)
            session.commit()
            session.refresh(stock)

        ts = TimeSeries(key=CONFIG["alpha_vantage"]["key"])
        data, _ = ts.get_daily_adjusted(symbol, outputsize=outputsize)
        
        data_date = [date for date in data.keys()]
        data_date.reverse()
        data_close_price = [float(data[date][CONFIG["alpha_vantage"]["key_adjusted_close"]]) for date in data.keys()]
        data_close_price.reverse()

        data_points = []
        for date_str, price in zip(data_date, data_close_price):
            dp = DataPoint(stock_id=stock.id, date=date_str, adjusted_close=price)
            session.add(dp)
            data_points.append(dp)
        session.commit()

        norm_result = normalize_data(data_points, session)
        dataset_result = prepare_dataset(
            stock_id=stock.id,
            normalized_data=norm_result["normalized_values"],
            window_size=CONFIG["data"]["window_size"],
            train_split_size=CONFIG["data"]["train_split_size"],
            scaler=norm_result["scaler"],
            session=session
        )

        num_data_points = len(data_date)
        date_range = f"from {data_date[0]} to {data_date[-1]}"
        return {
            "symbol": symbol,
            "data_points": data_points,
            "num_data_points": num_data_points,
            "date_range": date_range,
            "dataset_id": dataset_result["dataset_id"]
        }

acquisition_service = AcquisitionService()