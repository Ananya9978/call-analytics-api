# Sales Call Analytics Microservice

This microservice analyzes **sales call transcripts** using FastAPI, SQLite, and NLP models for sentiment and embedding analysis. You can ingest, store, and query call data using a RESTful API.

---

##  Project Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/sales-call-analytics.git
cd sales-call-analytics

2. Set Up Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt

4. Create .env File
Create a .env file in the project root (same level as app/):

env
Copy
Edit
DATABASE_URL=sqlite:///./call_db.sqlite3
Tip: Use SQLite for local development. Replace with PostgreSQL URL for production.

# Initialize the Database
bash
Copy
Edit
python
>>> from app.models import Base
>>> from app.database import engine
>>> Base.metadata.create_all(bind=engine)
>>> exit()

# Ingest Fake Call Data
bash
Copy
Edit
python ingest_calls.py
This will generate 200 synthetic sales call transcripts and store them in the database.

# Run the FastAPI Server
bash
Copy
Edit
uvicorn app.main:app --reload
Then open: http://127.0.0.1:8000/docs


 Example API Requests (via curl)


# Get All Calls
bash
Copy
Edit
curl "http://localhost:8000/api/v1/calls?limit=5"

# Get Call by ID
bash
Copy
Edit
curl "http://localhost:8000/api/v1/calls/<CALL_ID>"

# Filter by Agent ID and Sentiment
bash
Copy
Edit
curl "http://localhost:8000/api/v1/calls?agent_id=agent_1&min_sentiment=0.0"

# Get Recommendations for a Call
bash
Copy
Edit
curl "http://localhost:8000/api/v1/calls/<CALL_ID>/recommendations"


# Get Analytics Leaderboard
bash
Copy
Edit
curl "http://localhost:8000/api/v1/analytics/agents"


# Test with Pytest
bash
Copy
Edit
pytest --cov=app tests/

# Makefile Shortcut
Create a Makefile with:

makefile
Copy
Edit
dev-up:
	uvicorn app.main:app --reload
Then run:

bash
Copy
Edit
make dev-up

# Assumptions & Trade-Offs
Used SQLite for simplicity (not scalable for high concurrency).

Synthetic data is generated using faker instead of real transcripts.

Embeddings and sentiment are computed once and stored to avoid recomputation.

No authentication added — easily extendable with JWT middleware.

The recommendation engine uses cosine similarity on sentence embeddings.

Full-text search and advanced analytics are omitted for SQLite compatibility.