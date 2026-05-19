from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import goals, agents, sponsorships, search, websocket
from app.utils.logger import get_logger
from app.services.embedding_service import init_embedding_service, get_embedding_service
from app.services.search_service import init_search_service
from app.api.deps import AsyncSessionLocal

logger = get_logger(__name__)

app = FastAPI(title="Throne Travel API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(goals.router, prefix="/api/goals", tags=["goals"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(sponsorships.router, prefix="/api/sponsorships", tags=["sponsorships"])
app.include_router(search.router, prefix="/api/routes", tags=["routes"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])


@app.on_event("startup")
async def startup_event():
    """Initialize AI and search services on startup."""
    # Embedding service (Gemini)
    try:
        await init_embedding_service(
            api_key=settings.gemini_api_key,
            redis_url=settings.redis_url,
        )
        logger.info("✅ EmbeddingService initialized")
    except Exception as e:
        logger.error(f"❌ EmbeddingService init failed: {e}")
        raise

    # Search service (Hybrid vector+filter)
    try:
        async with AsyncSessionLocal() as session:
            embedding_svc = get_embedding_service()
            await init_search_service(
                session=session,
                embedding_service=embedding_svc,
            )
        logger.info("✅ SearchService initialized")
    except Exception as e:
        logger.error(f"❌ SearchService init failed: {e}")
        raise


@app.get("/health")
async def health():
    return {"status": "ok"}
