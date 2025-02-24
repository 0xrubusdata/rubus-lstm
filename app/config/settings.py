from dotenv import load_dotenv
import os
from sqlmodel import create_engine, Session
from app.config.defaults import ALPHA_VANTAGE_KEY, CONFIG
from app.services.config.config_service import config_service

load_dotenv()

POSTGRES_USER=os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB=os.getenv("POSTGRES_DB", "fastapi_db")
POSTGRES_PORT=os.getenv("POSTGRES_PORT", 5432)
                                        
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@lstm-postgres:{POSTGRES_PORT}/{POSTGRES_DB}"