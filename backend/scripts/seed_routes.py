"""Seed 20 sample routes with embeddings into the database."""
import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings
from app.models.db import Route
from app.services.embedding_service import embed_text

SAMPLE_ROUTES = [
    ("Istanbul", "Paris", "Romantic city break with art, cuisine and river walks."),
    ("Istanbul", "Tokyo", "East meets Far East — temples, ramen, and neon lights."),
    ("Ankara", "Barcelona", "Beach, Gaudi architecture and tapas culture."),
    ("Istanbul", "New York", "The city that never sleeps awaits — Broadway to Brooklyn."),
    ("Izmir", "Amsterdam", "Canals, tulips, bikes and world-class museums."),
    ("Istanbul", "Dubai", "Desert luxury, skyscrapers and souks."),
    ("Ankara", "London", "History, theatre and afternoon tea."),
    ("Istanbul", "Bali", "Spiritual retreats, rice paddies and ocean sunsets."),
    ("Istanbul", "Prague", "Medieval castles and craft beer culture."),
    ("Istanbul", "Lisbon", "Fado music, pastel de nata and Atlantic views."),
]


async def main():
    engine = create_async_engine(
        settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
    )
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        for origin, dest, desc in SAMPLE_ROUTES:
            embedding = await embed_text(f"{origin} to {dest}: {desc}")
            route = Route(
                id=str(uuid.uuid4()),
                origin=origin,
                destination=dest,
                description_md=desc,
                tags="featured",
                embedding=embedding,
            )
            session.add(route)
        await session.commit()
    print(f"Seeded {len(SAMPLE_ROUTES)} routes.")


if __name__ == "__main__":
    asyncio.run(main())
