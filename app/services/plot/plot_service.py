from sqlmodel import Session, select
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from datetime import timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.utils.normalizer import Normalizer
    from app.models import TrainingRun, Prediction, Stock, DataPoint, Dataset
    from app.config.settings import CONFIG

class ServePlotsService:
    @staticmethod
    def plot_prices(training_run_id: int, plot_type: str, session: Session) -> str:
        training_run = session.get(TrainingRun, training_run_id)
        if not training_run:
            raise ValueError("Training run not found")

        model_config = session.get(ModelConfig, training_run.model_config_id)
        stock = session.get(Stock, model_config.stock_id)
        dataset = session.get(Dataset, training_run.dataset_id)
        if not model_config or not stock or not dataset:
            raise ValueError("Model config, stock, or dataset not found")

        # Reconstruct scaler
        scaler = Normalizer()
        scaler.mu = np.array([dataset.scaler_mu])
        scaler.sd = np.array([dataset.scaler_sd])

        xticks_interval = CONFIG["plots"]["xticks_interval"]
        colors = {
            "actual": "#001f3f",
            "train": "#3D9970",
            "val": "#0074D9",
            "pred_train": "#3D9970",
            "pred_val": "#0074D9",
            "pred_test": "#FF4136"
        }

        fig = figure(figsize=(25, 5), dpi=80)
        fig.patch.set_facecolor((1.0, 1.0, 1.0))

        if plot_type == "actual_vs_predicted":
            ServePlotsService._plot_actual_vs_predicted(
                session, training_run, stock, xticks_interval, colors, plt
            )
        elif plot_type == "train_vs_val":
            ServePlotsService._plot_train_vs_val(
                session, dataset, stock, scaler, xticks_interval, colors, plt
            )
        elif plot_type == "zoom_val":
            ServePlotsService._plot_zoom_val(
                session, training_run, stock, xticks_interval, colors, plt
            )
        elif plot_type == "next_day":
            ServePlotsService._plot_next_day(
                session, training_run, stock, xticks_interval, colors, plt
            )
        else:
            raise ValueError(f"Unsupported plot type: {plot_type}")

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        return image_base64

    @staticmethod
    def _plot_actual_vs_predicted(session, training_run, stock, xticks_interval, colors, plt):
        predictions = session.exec(
            select(Prediction).where(Prediction.training_run_id == training_run.id)
        ).all()
        if not predictions:
            raise ValueError("No predictions found")

        dates = [p.date for p in predictions]
        actual_prices = np.array([p.actual_price if p.actual_price is not None else np.nan for p in predictions])
        predicted_prices = np.array([p.predicted_price for p in predictions])

        plt.plot(dates, actual_prices, label="Actual prices", color=colors["actual"])
        plt.plot(dates, predicted_prices, label="Predicted prices (validation)", color=colors["pred_val"])

        num_data_points = len(dates)
        xticks = [
            dates[i] if (
                (i % xticks_interval == 0 and (num_data_points - i) > xticks_interval) or i == num_data_points - 1
            ) else None
            for i in range(num_data_points)
        ]
        x = np.arange(0, len(xticks))
        plt.xticks(x, [d.strftime('%Y-%m-%d') if d else '' for d in xticks], rotation='vertical')
        plt.title(f"Actual vs Predicted Prices for {stock.symbol}")
        plt.grid(b=None, which='major', axis='y', linestyle='--')
        plt.legend()

    @staticmethod
    def _plot_train_vs_val(session, dataset, stock, scaler, xticks_interval, colors, plt):
        # Load persisted datasets
        train_dataset = torch.load(dataset.train_dataset_path)
        val_dataset = torch.load(dataset.val_dataset_path)

        # Fetch all data points for dates
        data_points = session.exec(
            select(DataPoint).where(DataPoint.stock_id == stock.id)
        ).all()
        dates = [dp.date for dp in data_points]
        num_data_points = len(dates)

        # Prepare plotting arrays
        to_plot_train = np.zeros(num_data_points)
        to_plot_val = np.zeros(num_data_points)
        train_len = len(train_dataset.y)
        val_len = len(val_dataset.y)
        window_size = dataset.window_size
        split_index = int((num_data_points - window_size) * dataset.train_split_size)

        # Inverse transform and place data
        to_plot_train[window_size:split_index + window_size] = scaler.inverse_transform(train_dataset.y.numpy())
        to_plot_val[split_index + window_size:split_index + window_size + val_len] = scaler.inverse_transform(val_dataset.y.numpy())
        to_plot_train = np.where(to_plot_train == 0, np.nan, to_plot_train)
        to_plot_val = np.where(to_plot_val == 0, np.nan, to_plot_val)

        plt.plot(dates, to_plot_train, label="Prices (train)", color=colors["train"])
        plt.plot(dates, to_plot_val, label="Prices (validation)", color=colors["val"])

        xticks = [
            dates[i] if (
                (i % xticks_interval == 0 and (num_data_points - i) > xticks_interval) or i == num_data_points - 1
            ) else None
            for i in range(num_data_points)
        ]
        x = np.arange(0, len(xticks))
        plt.xticks(x, [d.strftime('%Y-%m-%d') if d else '' for d in xticks], rotation='vertical')
        plt.title(f"Training vs Validation Prices for {stock.symbol}")
        plt.grid(b=None, which='major', axis='y', linestyle='--')
        plt.legend()

    @staticmethod
    def _plot_zoom_val(session, training_run, stock, xticks_interval, colors, plt):
        predictions = session.exec(
            select(Prediction).where(Prediction.training_run_id == training_run.id)
        ).all()
        if not predictions:
            raise ValueError("No predictions found")

        dates = [p.date for p in predictions]
        actual_prices = np.array([p.actual_price if p.actual_price is not None else np.nan for p in predictions])
        predicted_prices = np.array([p.predicted_price for p in predictions])

        plt.plot(dates, actual_prices, label="Actual prices", color=colors["actual"])
        plt.plot(dates, predicted_prices, label="Predicted prices (validation)", color=colors["pred_val"])

        num_data_points = len(dates)
        reduced_interval = int(xticks_interval / 5)
        xticks = [
            dates[i] if (
                (i % reduced_interval == 0 and (num_data_points - i) > reduced_interval) or i == num_data_points - 1
            ) else None
            for i in range(num_data_points)
        ]
        x = np.arange(0, len(xticks))
        plt.xticks(x, [d.strftime('%Y-%m-%d') if d else '' for d in xticks], rotation='vertical')
        plt.title(f"Zoomed Validation Prices for {stock.symbol}")
        plt.grid(b=None, which='major', axis='y', linestyle='--')
        plt.legend()

    @staticmethod
    def _plot_next_day(session, training_run, stock, xticks_interval, colors, plt):
        predictions = session.exec(
            select(Prediction)
            .where(Prediction.training_run_id == training_run.id)
            .order_by(Prediction.date.desc())
            .limit(10)
        ).all()
        if not predictions:
            raise ValueError("No predictions found")

        dates = [p.date for p in predictions[::-1]]
        actual_prices = np.array([p.actual_price if p.actual_price is not None else np.nan for p in predictions[::-1]])
        predicted_prices = np.array([p.predicted_price for p in predictions[::-1]])

        last_date = dates[-1]
        tomorrow = last_date + timedelta(days=1)
        dates[-1] = tomorrow
        plot_dates = dates[-10:]

        to_plot_actual = actual_prices[-10:]
        to_plot_pred = predicted_prices[-10:]
        plt.plot(plot_dates, to_plot_actual, label="Actual prices", marker=".", markersize=10, color=colors["actual"])
        plt.plot(plot_dates, to_plot_pred, label="Predicted prices", marker=".", markersize=10, color=colors["pred_val"])
        plt.plot(plot_dates[-1:], to_plot_pred[-1:], label="Predicted next day", marker=".", markersize=20, color=colors["pred_test"])

        plt.xticks([d.strftime('%Y-%m-%d') for d in plot_dates], rotation='vertical')
        plt.title(f"Next Day Prediction for {stock.symbol}")
        plt.grid(b=None, which='major', axis='y', linestyle='--')
        plt.legend()

serve_plots_service = ServePlotsService()