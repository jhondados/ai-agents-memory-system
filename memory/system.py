"""Cognitive memory system for AI agents."""
from datetime import datetime, timedelta
from typing import List, Optional
import json, math
import redis
from pgvector.psycopg2 import register_vector
import psycopg2
import numpy as np

class AgentMemorySystem:
    def __init__(self, redis_url: str, pg_dsn: str):
        self.redis = redis.from_url(redis_url)
        self.conn = psycopg2.connect(pg_dsn)
        register_vector(self.conn)
        self._init_tables()

    def _init_tables(self):
        with self.conn.cursor() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS episodic_memory (
                id SERIAL PRIMARY KEY, agent_id TEXT, content TEXT,
                embedding vector(1536), importance FLOAT DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT NOW(), last_accessed TIMESTAMP DEFAULT NOW(),
                access_count INT DEFAULT 0)""")
            self.conn.commit()

    def remember(self, agent_id: str, content: str, embedding: List[float], importance: float = 0.5):
        with self.conn.cursor() as c:
            c.execute("INSERT INTO episodic_memory (agent_id, content, embedding, importance) VALUES (%s,%s,%s,%s)",
                (agent_id, content, embedding, importance))
            self.conn.commit()

    def recall(self, agent_id: str, query_embedding: List[float], top_k: int = 5) -> List[str]:
        with self.conn.cursor() as c:
            c.execute("""SELECT content, importance, created_at FROM episodic_memory
                WHERE agent_id=%s ORDER BY embedding <=> %s::vector LIMIT %s""",
                (agent_id, query_embedding, top_k))
            results = c.fetchall()
        return [r[0] for r in results]

    def ebbinghaus_strength(self, created_at: datetime, access_count: int, importance: float) -> float:
        """Memory strength based on forgetting curve."""
        days_old = (datetime.now() - created_at).days
        stability = importance * (1 + math.log(1 + access_count))
        return math.exp(-days_old / (stability * 30))
