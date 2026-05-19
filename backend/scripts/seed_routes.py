"""Seed 20 sample routes with Gemini embeddings into the database."""
import asyncio
import os
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

from app.config import settings
from app.models.db import Route
from app.services.embedding_service import (
    init_embedding_service,
    EmbeddingService,
    TASK_TYPE_DOCUMENT,
)

load_dotenv()

SAMPLE_ROUTES = [
    {
        "origin": "Istanbul",
        "destination": "Paris",
        "desc": "Romantic city break with art, cuisine and river walks.",
        "tags": ["romantic", "art", "culture", "europe"],
        "budget": 2500,
    },
    {
        "origin": "Istanbul",
        "destination": "Tokyo",
        "desc": "East meets Far East — temples, ramen, and neon lights.",
        "tags": ["adventure", "asia", "food"],
        "budget": 3500,
    },
    {
        "origin": "Ankara",
        "destination": "Barcelona",
        "desc": "Beach, Gaudi architecture and tapas culture.",
        "tags": ["beach", "architecture", "food"],
        "budget": 2800,
    },
    {
        "origin": "Istanbul",
        "destination": "New York",
        "desc": "The city that never sleeps — Broadway to Brooklyn.",
        "tags": ["urban", "culture", "food", "america"],
        "budget": 4000,
    },
    {
        "origin": "Izmir",
        "destination": "Amsterdam",
        "desc": "Canals, tulips, bikes and world-class museums.",
        "tags": ["canal", "museum", "bike", "europe"],
        "budget": 2200,
    },
    {
        "origin": "Istanbul",
        "destination": "Dubai",
        "desc": "Desert luxury, skyscrapers and souks.",
        "tags": ["luxury", "desert", "middle-east"],
        "budget": 3000,
    },
    {
        "origin": "Ankara",
        "destination": "London",
        "desc": "History, theatre and afternoon tea.",
        "tags": ["history", "culture", "europe"],
        "budget": 2600,
    },
    {
        "origin": "Istanbul",
        "destination": "Bali",
        "desc": "Spiritual retreats, rice paddies and ocean sunsets.",
        "tags": ["spiritual", "beach", "asia", "relax"],
        "budget": 1800,
    },
    {
        "origin": "Istanbul",
        "destination": "Prague",
        "desc": "Medieval castles and craft beer culture.",
        "tags": ["history", "beer", "europe", "castle"],
        "budget": 2100,
    },
    {
        "origin": "Istanbul",
        "destination": "Lisbon",
        "desc": "Fado music, pastel de nata and Atlantic views.",
        "tags": ["music", "food", "beach", "europe"],
        "budget": 1900,
    },
]


async def main():
    """Seed routes with embeddings."""
    print("=" * 60)
    print("🌍 Seeding Routes with Gemini Embeddings")
    print("=" * 60)

    # Embedding service init
    gemini_key = os.getenv("GEMINI_API_KEY")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    if not gemini_key:
        print("❌ GEMINI_API_KEY not set in .env")
        return

    embedding_svc = await init_embedding_service(
        api_key=gemini_key,
        redis_url=redis_url,
    )

    # DB connection
    engine = create_async_engine(
        settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        for i, route_data in enumerate(SAMPLE_ROUTES, 1):
            origin = route_data["origin"]
            dest = route_data["destination"]
            desc = route_data["desc"]
            tags = ",".join(route_data["tags"])

            # Format for embedding
            text = EmbeddingService.format_route_for_embedding(
                destination=dest,
                duration_days=5,  # Demo: 5 days
                estimated_budget_usd=route_data["budget"],
                tags=route_data["tags"],
                description=desc,
            )

            # Embed
            print(f"[{i}/{len(SAMPLE_ROUTES)}] Embedding: {origin} → {dest}...", end=" ")
            emb_result = await embedding_svc.embed_document(text)

            # Create route
            route = Route(
                id=str(uuid.uuid4()),
                origin=origin,
                destination=dest,
                description_md=desc,
                tags=tags,
                embedding=emb_result.vector,
                creator_wallet="seed@demo",
                copy_count=i,  # Demo: increasing popularity
            )
            session.add(route)
            print("✓")

        await session.commit()
        print(f"\n✅ Seeded {len(SAMPLE_ROUTES)} routes with embeddings!")
        print(f"📊 Total API calls: {embedding_svc.total_requests}")


if __name__ == "__main__":
    asyncio.run(main())
