import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Call
from app.ai import compute_embedding, compute_sentiment, compute_talk_ratio
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

with open("data/raw_calls.json") as f:
    calls = json.load(f)

for item in calls:
    transcript = item["transcript"]
    call = Call(
        call_id=item["call_id"],
        agent_id=item["agent_id"],
        customer_id=item["customer_id"],
        language=item["language"],
        start_time=datetime.fromisoformat(item["start_time"]),
        duration_seconds=item["duration_seconds"],
        transcript=transcript,
        agent_talk_ratio=compute_talk_ratio(transcript),
        customer_sentiment_score=compute_sentiment(transcript),
        embedding=json.dumps(compute_embedding(transcript)),
    )
    session.add(call)

session.commit()
