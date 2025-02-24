# app/config/defaults.py
import os

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "YOUR_API_KEY")

CONFIG = {
    "alpha_vantage": {"key": ALPHA_VANTAGE_KEY, "key_adjusted_close": "5. adjusted close"},
    "data": {"window_size": 20, "train_split_size": 0.80},
    "plots": {"xticks_interval": 90},
    "training": {
        "batch_size": 64,
        "num_epoch": 100,
        "learning_rate": 0.01,
        "scheduler_step_size": 40,
        "device": "cpu"
    }
}
