"""
Redis caching service for adaptive learning data.

Caches:
- Knowledge state: 5 minute TTL (per student)
- Knowledge graph: 1 hour TTL (shared)
- Recommendations: 2 minute TTL (per student)
"""

import json
import logging
from typing import Any

import redis.asyncio as redis

from app.config import settings

logger = logging.getLogger(__name__)

# TTL constants (seconds)
KNOWLEDGE_STATE_TTL = 300   # 5 minutes
KNOWLEDGE_GRAPH_TTL = 3600  # 1 hour
RECOMMENDATIONS_TTL = 120   # 2 minutes

# Key prefixes
KS_PREFIX = "ks:"           # knowledge state
KG_KEY = "kg:graph"          # knowledge graph (shared)
REC_PREFIX = "rec:"          # recommendations


class CacheService:
    """Async Redis cache for adaptive learning data."""

    def __init__(self):
        self._redis: redis.Redis | None = None

    async def connect(self):
        """Initialize Redis connection."""
        try:
            self._redis = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=3,
            )
            await self._redis.ping()
            logger.info("Redis cache connected")
        except Exception as e:
            logger.warning(f"Redis not available, caching disabled: {e}")
            self._redis = None

    async def close(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.aclose()

    async def get(self, key: str) -> Any | None:
        """Get cached value, returns None on miss or error."""
        if not self._redis:
            return None
        try:
            data = await self._redis.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.debug(f"Cache get error for {key}: {e}")
        return None

    async def set(self, key: str, value: Any, ttl: int = 300):
        """Set cached value with TTL."""
        if not self._redis:
            return
        try:
            await self._redis.setex(key, ttl, json.dumps(value, default=str))
        except Exception as e:
            logger.debug(f"Cache set error for {key}: {e}")

    async def delete(self, key: str):
        """Delete a cached key."""
        if not self._redis:
            return
        try:
            await self._redis.delete(key)
        except Exception as e:
            logger.debug(f"Cache delete error for {key}: {e}")

    async def invalidate_student(self, student_id: str):
        """Invalidate all cached data for a student (after submission update)."""
        await self.delete(f"{KS_PREFIX}{student_id}")
        await self.delete(f"{REC_PREFIX}{student_id}")

    # --- Domain-specific helpers ---

    async def get_knowledge_state(self, student_id: str) -> dict | None:
        return await self.get(f"{KS_PREFIX}{student_id}")

    async def set_knowledge_state(self, student_id: str, data: dict):
        await self.set(f"{KS_PREFIX}{student_id}", data, KNOWLEDGE_STATE_TTL)

    async def get_knowledge_graph(self) -> dict | None:
        return await self.get(KG_KEY)

    async def set_knowledge_graph(self, data: dict):
        await self.set(KG_KEY, data, KNOWLEDGE_GRAPH_TTL)

    async def get_recommendations(self, student_id: str) -> dict | None:
        return await self.get(f"{REC_PREFIX}{student_id}")

    async def set_recommendations(self, student_id: str, data: dict):
        await self.set(f"{REC_PREFIX}{student_id}", data, RECOMMENDATIONS_TTL)


# Singleton instance
cache = CacheService()
