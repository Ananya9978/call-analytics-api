from fastapi import FastAPI, HTTPException, Query
from app.models import Call, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_
from typing import List
from dotenv import load_dotenv
import os, json
from datetime import datetime
from pathlib import Path

load_dotenv()
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
# SQLite-friendly engine
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set. Did you forget the .env file?")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

Session = sessionmaker(bind=engine)

app = FastAPI()

@app.get("/api/v1/calls")
def get_calls(limit: int = 10, offset: int = 0,
              agent_id: str = None,
              from_date: str = None,
              to_date: str = None,
              min_sentiment: float = -1.0,
              max_sentiment: float = 1.0):
    session = Session()
    query = session.query(Call)
    
    if agent_id:
        query = query.filter(Call.agent_id == agent_id)
    if from_date:
        query = query.filter(Call.start_time >= datetime.fromisoformat(from_date))
    if to_date:
        query = query.filter(Call.start_time <= datetime.fromisoformat(to_date))
    
    query = query.filter(Call.customer_sentiment_score.between(min_sentiment, max_sentiment))
    return query.offset(offset).limit(limit).all()

@app.get("/api/v1/calls/{call_id}")
def get_call(call_id: str):
    session = Session()
    call = session.query(Call).filter(Call.call_id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call
