from sqlmodel import Session, select
import torch
import numpy as np

from app.models.normalized_data import NormalizedData
from app.services.data.factory.alpha_vantage_factory import alpha_vantage_factory
from app.utils.normalizer import Normalizer
from app.models import Stock, DataPoint
from app.config.settings import CONFIG

class AcquisitionService:
    @staticmethod
    def acquire_data(symbol: str, data_source: str, outputsize: str, session: Session):
        # Check or create stock (assuming symbol is relevant across data sources)
        stock = session.exec(select(Stock).where(Stock.symbol == symbol)).first()
        if not stock:
            stock = Stock(symbol=symbol)
            session.add(stock)
            session.commit()
            session.refresh(stock)

        # Get the appropriate Alpha Vantage service
        service = alpha_vantage_factory.get_service(data_source)

        # Fetch data based on source (focus on time-series-like data for LSTM)
        if data_source == "timeseries":
            data, _ = service.get_daily_adjusted(symbol, outputsize=outputsize)
            key_value = CONFIG["alpha_vantage"]["key_adjusted_close"]
        elif data_source == "cryptocurrencies":
            data, _ = service.get_daily(symbol, market="USD", outputsize=outputsize)
            key_value = "4b. close (USD)"  # Adjust based on Alpha Vantage response
        elif data_source == "foreignexchange":
            data, _ = service.get_daily(from_symbol=symbol[:3], to_symbol=symbol[3:], outputsize=outputsize)
            key_value = "4. close"
        else:
            # Placeholder for non-time-series data; extend as needed
            raise ValueError(f"Data source '{data_source}' not yet supported for time-series prediction")

        # Extract and reverse data
        data_date = [date for date in data.keys()]
        data_date.reverse()
        data_close_price = [float(data[date][key_value]) for date in data.keys()]
        data_close_price.reverse()

        # Persist raw data as DataPoints
        data_points = []
        for date_str, price in zip(data_date, data_close_price):
            dp = DataPoint(stock_id=stock.id, date=date_str, adjusted_close=price)
            session.add(dp)
            data_points.append(dp)
        session.commit()

        # Normalize and prepare dataset
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
    
    @staticmethod
    def normalize_data(data_points: list[DataPoint], session: Session):
        raw_prices = np.array([dp.adjusted_close for dp in data_points])
        scaler = Normalizer()
        normalized_prices = scaler.fit_transform(raw_prices)

        normalized_data = []
        for dp, norm_value in zip(data_points, normalized_prices):
            nd = NormalizedData(
                dataset_id=None,
                data_point_id=dp.id,
                normalized_value=float(norm_value)
            )
            session.add(nd)
            normalized_data.append(nd)
        session.commit()

        return {
            "scaler": scaler,
            "normalized_values": normalized_prices,
            "normalized_data": normalized_data
        }
    
    @staticmethod
    def prepare_data_x(x: np.ndarray, window_size: int):
        n_row = x.shape[0] - window_size + 1
        output = np.lib.stride_tricks.as_strided(x, shape=(n_row, window_size), strides=(x.strides[0], x.strides[0]))
        return output[:-1], output[-1]

    @staticmethod
    def prepare_data_y(x: np.ndarray, window_size: int):
        return x[window_size:]

    @staticmethod
    def prepare_dataset(stock_id: int, normalized_data: np.ndarray, window_size: int, train_split_size: float, scaler: Normalizer, session: Session):
        # Create Dataset entry with scaler state
        dataset = Dataset(
            stock_id=stock_id,
            window_size=window_size,
            train_split_size=train_split_size,
            scaler_mu=float(scaler.mu[0]),  # Assuming 1D data
            scaler_sd=float(scaler.sd[0])
        )
        session.add(dataset)
        session.commit()
        session.refresh(dataset)

        # Window data
        data_x, data_x_unseen = DatasetPrepService.prepare_data_x(normalized_data, window_size)
        data_y = DatasetPrepService.prepare_data_y(normalized_data, window_size)

        # Split into train/val
        split_index = int(data_y.shape[0] * train_split_size)
        data_x_train = data_x[:split_index]
        data_x_val = data_x[split_index:]
        data_y_train = data_y[:split_index]
        data_y_val = data_y[split_index:]

        # Update NormalizedData with dataset_id
        norm_data = session.exec(select(NormalizedData).where(NormalizedData.dataset_id.is_(None))).all()
        for nd in norm_data[:len(normalized_data)]:
            nd.dataset_id = dataset.id
        session.commit()

        # Create and save PyTorch datasets
        train_dataset = TimeSeriesDataset(data_x_train, data_y_train)
        val_dataset = TimeSeriesDataset(data_x_val, data_y_val)

        # Persist datasets to disk
        os.makedirs("datasets", exist_ok=True)
        train_path = f"datasets/train_{dataset.id}.pt"
        val_path = f"datasets/val_{dataset.id}.pt"
        torch.save(train_dataset, train_path)
        torch.save(val_dataset, val_path)

        dataset.train_dataset_path = train_path
        dataset.val_dataset_path = val_path
        session.commit()

        return {
            "dataset_id": dataset.id,
            "train_dataset": train_dataset,
            "val_dataset": val_dataset,
            "data_x_unseen": data_x_unseen,
            "scaler": scaler
        }

acquisition_service = AcquisitionService()