from app.models import Call, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Add a sample call
sample_call = Call(
    call_id="call_001",
    agent_id="agent_123",
    customer_id="cust_456",
    language="en",
    start_time=datetime.now(),
    duration_seconds=320,
    transcript="Agent: Hello, how can I help you? Customer: I need support with my account.",
    agent_talk_ratio=0.6,
    customer_sentiment_score=0.4,
    embedding=[0.1] * 384  # dummy 384-d vector
)

session.add(sample_call)
session.commit()
print("Sample call added.")
