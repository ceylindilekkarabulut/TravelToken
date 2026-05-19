import math
import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models.db import Route
from app.models.schemas import RouteResponse
from app.services.embedding_service import embed_text

router = APIRouter()


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _keyword_score(route: Route, query: str) -> float:
    score = 0.0
    lower = query.lower()
    if route.origin.lower() in lower or route.destination.lower() in lower:
        score += 0.18
    if route.tags and any(tag.strip() and tag.strip() in lower for tag in route.tags.lower().split(",")):
        score += 0.12
    if route.description_md and route.description_md.lower() in lower:
        score += 0.05
    return score


@router.get("/search")
async def search_routes(query: str = "", limit: int = 10, db: AsyncSession = Depends(get_db)):
    if not query.strip():
        result = await db.execute(select(Route).order_by(Route.copy_count.desc()).limit(limit))
        return result.scalars().all()

    embedding = await embed_text(query)
    result = await db.execute(select(Route).limit(200))
    routes = result.scalars().all()

    scored = []
    for route in routes:
        score = _cosine_similarity(route.embedding or [], embedding)
        score += _keyword_score(route, query)
        scored.append((score, route))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [route for _, route in scored[:limit]]


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(route_id: str, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.post("/{route_id}/copy")
async def copy_route(route_id: str, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if route:
        route.copy_count += 1
        await db.commit()
    return {"route_id": route_id, "copy_count": route.copy_count if route else 0}
