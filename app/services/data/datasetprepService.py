from sqlmodel import Session, select
from app.models import Dataset, NormalizedData
from app.utils.dataset import TimeSeriesDataset
from app.utils.normalizer import Normalizer
import numpy as np
import torch
import os

class DatasetPrepService:
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

datasetprep_service = DatasetPrepService()