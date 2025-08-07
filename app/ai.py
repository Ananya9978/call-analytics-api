from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np

embedder = SentenceTransformer('all-MiniLM-L6-v2')
sentiment_analyzer = pipeline("sentiment-analysis")

def compute_embedding(text: str) -> list[float]:
    return embedder.encode(text).tolist()

def compute_sentiment(text: str) -> float:
    result = sentiment_analyzer(text[:512])[0]
    score = result['score']
    return score if result['label'] == 'POSITIVE' else -score

def compute_talk_ratio(transcript: str) -> float:
    agent_words = sum(len(p.split()) for p in transcript.split("customer:")[0].split("agent:")[1:])
    total_words = sum(len(p.split()) for p in transcript.split(":")[1:])
    return round(agent_words / total_words, 2) if total_words else 0.0
