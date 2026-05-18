from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import goals, agents, sponsorships, search, websocket
from app.utils.logger import get_logger

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


@app.get("/health")
async def health():
    return {"status": "ok"}
