"""Pre-warm Redis cache with popular route searches."""
import asyncio
import redis.asyncio as aioredis
import json
from app.config import settings

POPULAR_QUERIES = [
    "Istanbul to Paris cheap flights",
    "Istanbul to Tokyo budget trip",
    "beach vacation Europe",
    "cultural trip Asia",
]


async def main():
    r = aioredis.from_url(settings.redis_url)
    for query in POPULAR_QUERIES:
        key = f"search:{query}"
        existing = await r.get(key)
        if not existing:
            await r.setex(key, 3600, json.dumps({"query": query, "results": []}))
            print(f"Warmed: {key}")
    await r.aclose()


if __name__ == "__main__":
    asyncio.run(main())
