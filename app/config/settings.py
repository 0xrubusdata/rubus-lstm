from dotenv import load_dotenv
import os
from sqlmodel import create_engine, Session
from app.services.config.configService import config_service

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/stock_db")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "YOUR_API_KEY")

# Initial config (will be overridden by DB if present)
CONFIG = {
    "alpha_vantage": {"key": ALPHA_VANTAGE_KEY, "key_adjusted_close": "5. adjusted close"},
    "data": {"window_size": 20, "train_split_size": 0.80},
    "plots": {"xticks_interval": 90},
    "training": {"batch_size": 64, "num_epoch": 100, "learning_rate": 0.01, "scheduler_step_size": 40, "device": "cpu"}
}

# Load from DB on startup
engine = create_engine(DATABASE_URL)
with Session(engine) as session:
    db_config = config_service.get_config(session)
    CONFIG["alpha_vantage"]["key"] = db_config["alpha_vantage_key"]
    CONFIG["plots"]["xticks_interval"] = db_config["xticks_interval"]