from dotenv import load_dotenv
import os
import time
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

# Configuration de la base de données
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fastapi_db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@lstm-postgres:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Créez les tables dans la base de données
def create_db_and_tables():
    time.sleep(5)  # Sleep for 5 seconds
    SQLModel.metadata.create_all(engine)