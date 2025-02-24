# app/main.py
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session
import time

from app.config.database import create_db_and_tables
from app.routes.config import router as config_router
from app.routes.data import router as acquire_router
from app.routes.model import router as model_router
from app.routes.plot import router as plot_router

load_dotenv()

app = FastAPI(
    title="Rubus LSTM API",
    description="API for stock price prediction using LSTM.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ajoutez cet événement au démarrage de l'application
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Inclusion des routers
app.include_router(config_router, tags=["Configuration"])
app.include_router(acquire_router, tags=["Data"])
app.include_router(model_router, tags=["Model"])
app.include_router(plot_router, tags=["Plot"])

# Vos routes API
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Autres routes...