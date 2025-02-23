from sqlmodel import Session, select
from app.models import TrainingRun, Prediction, Dataset, ModelConfig
from app.services.model.definitionService import definition_service
from app.config.settings import CONFIG
from app.utils.dataset import TimeSeriesDataset
import torch
from torch.utils.data import DataLoader
import numpy as np

class EvaluationService:
    @staticmethod
    def evaluate_model(training_run_id: int, session: Session):
        # Fetch training run and related data
        training_run = session.get(TrainingRun, training_run_id)
        if not training_run:
            raise ValueError("Training run not found")

        model_config = session.get(ModelConfig, training_run.model_config_id)
        dataset = session.get(Dataset, training_run.dataset_id)
        if not model_config or not dataset:
            raise ValueError("Model config or dataset not found")

        # Load the trained model
        model = definition_service.define_lstm_model(
            input_size=model_config.input_size,
            hidden_layer_size=model_config.lstm_size,
            num_layers=model_config.num_lstm_layers,
            dropout=model_config.dropout
        )
        model.load_state_dict(torch.load(training_run.model_state_path))
        model = model.to(CONFIG["training"]["device"])
        model.eval()

        # Placeholder: Fetch validation dataset (assume prepared earlier)
        # In practice, you'd store or regenerate this from datasetprep_service
        # For now, simulate with a simplified reload from your script logic
        data_points = session.exec(
            select(DataPoint)
            .join(Dataset, Dataset.stock_id == DataPoint.stock_id)
            .where(Dataset.id == dataset.id)
        ).all()
        raw_prices = np.array([dp.adjusted_close for dp in data_points])
        from app.services.data.normalizationService import normalization_service
        norm_result = normalization_service.normalize_data(data_points, session)
        scaler = norm_result["scaler"]
        normalized_data = norm_result["normalized_values"]

        from app.services.data.datasetprepService import datasetprep_service
        data_x, _ = datasetprep_service.prepare_data_x(normalized_data, dataset.window_size)
        data_y = datasetprep_service.prepare_data_y(normalized_data, dataset.window_size)
        split_index = int(data_y.shape[0] * dataset.train_split_size)
        data_x_val = data_x[split_index:]
        data_y_val = data_y[split_index:]
        val_dataset = TimeSeriesDataset(data_x_val, data_y_val)
        val_dataloader = DataLoader(val_dataset, batch_size=CONFIG["training"]["batch_size"], shuffle=False)

        # Generate predictions
        predicted_val = []
        with torch.no_grad():
            for x, y in val_dataloader:
                x = x.to(CONFIG["training"]["device"])
                out = model(x)
                predicted_val.extend(out.cpu().numpy())

        # Inverse transform predictions and actuals
        predicted_val = np.array(predicted_val)
        actual_val = scaler.inverse_transform(data_y_val)
        predicted_val = scaler.inverse_transform(predicted_val)

        # Persist predictions
        predictions = []
        offset = split_index + dataset.window_size  # Adjust for windowing
        for i, (actual, pred) in enumerate(zip(actual_val, predicted_val)):
            date = data_points[offset + i].date
            prediction = Prediction(
                training_run_id=training_run_id,
                date=date,
                actual_price=float(actual),
                predicted_price=float(pred)
            )
            session.add(prediction)
            predictions.append(prediction)
        session.commit()

        # Return results for the route
        return {
            "(predictions": [
                {"date": p.date, "actual_price": p.actual_price, "predicted_price": p.predicted_price}
                for p in predictions
            ]
        }

evaluation_service = EvaluationService()