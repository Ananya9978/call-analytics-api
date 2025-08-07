from datasets import load_dataset
import uuid, random
from datetime import datetime, timedelta
import json
from pathlib import Path

dataset = load_dataset("daily_dialog", split="train")

Path("data").mkdir(exist_ok=True)

calls = []
for i, item in enumerate(dataset.select(range(200))):
    turns = item['dialog']
    if not turns:
        continue

    transcript = " ".join([f"{'agent' if i % 2 == 0 else 'customer'}: {t}" for i, t in enumerate(turns)])
    calls.append({
        "call_id": str(uuid.uuid4()),
        "agent_id": str(uuid.uuid4()),
        "customer_id": str(uuid.uuid4()),
        "language": "en",
        "start_time": datetime.now().isoformat(),
        "duration_seconds": random.randint(60, 600),
        "transcript": transcript
    })

with open("data/raw_calls.json", "w") as f:
    json.dump(calls, f, indent=2)
print(f" Saved {len(calls)} fake call transcripts to data/raw_calls.json")