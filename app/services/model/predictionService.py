from sqlmodel import Session, select
from app.models import TrainingRun, Prediction, ModelConfig, DataPoint
from app.services.model.definitionService import definition_service
from app.config.settings import CONFIG
import torch
import numpy as np
from datetime import timedelta

class PredictionService:
    @staticmethod
    def predict_next_day(training_run_id: int, session: Session):
        # Fetch training run and related data
        training_run = session.get(TrainingRun, training_run_id)
        if not training_run:
            raise ValueError("Training run not found")

        model_config = session.get(ModelConfig, training_run.model_config_id)
        if not model_config:
            raise ValueError("Model config not found")

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

        # Fetch most recent data points for the stock
        data_points = session.exec(
            select(DataPoint)
            .where(DataPoint.stock_id == model_config.stock_id)
            .order_by(DataPoint.date.desc())
            .limit(CONFIG["data"]["window_size"])
        ).all()
        if len(data_points) < CONFIG["data"]["window_size"]:
            raise ValueError("Not enough data points for prediction")

        # Normalize recent data
        raw_prices = np.array([dp.adjusted_close for dp in data_points[::-1]])  # Reverse to chronological order
        from app.services.data.normalizationService import normalization_service
        norm_result = normalization_service.normalize_data(data_points, session)  # Simplified; ideally use same scaler
        scaler = norm_result["scaler"]
        normalized_data = norm_result["normalized_values"]

        # Prepare unseen data (last window)
        from app.services.data.datasetprepService import datasetprep_service
        data_x, data_x_unseen = datasetprep_service.prepare_data_x(normalized_data, CONFIG["data"]["window_size"])
        x_unseen = torch.tensor(data_x_unseen).float().to(CONFIG["training"]["device"]).unsqueeze(0).unsqueeze(2)

        # Predict
        with torch.no_grad():
            prediction = model(x_unseen)
            predicted_price = scaler.inverse_transform(prediction.cpu().numpy())[0]

        # Determine "tomorrow's" date
        last_date = data_points[0].date  # Most recent date (desc order)
        tomorrow = last_date + timedelta(days=1)

        # Persist prediction
        prediction_entry = Prediction(
            training_run_id=training_run_id,
            date=tomorrow,
            actual_price=None,  # Unknown until later
            predicted_price=float(predicted_price)
        )
        session.add(prediction_entry)
        session.commit()

        # Return result for the route
        return {
            "date": tomorrow,
            "predicted_price": float(predicted_price)
        }

prediction_service = PredictionService()