from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.db import Route
from app.models.schemas import RouteResponse
from app.services.search_service import (
    get_search_service,
    SearchService,
    SearchFilter,
)

router = APIRouter()


@router.get("/search", response_model=list[RouteResponse])
async def search_routes(
    q: str = Query(..., min_length=1, description="Search query"),
    origin: Optional[str] = Query(None, description="Filter by origin city"),
    tags: Optional[list[str]] = Query(None, description="Filter by tags"),
    limit: int = Query(10, ge=1, le=50, description="Result limit"),
    search_svc: SearchService = Depends(get_search_service),
) -> list[RouteResponse]:
    """
    Hybrid vector + metadata search for routes.

    - Embeds query using Gemini
    - Performs HNSW similarity search
    - Applies metadata filters (origin, tags)
    - Re-ranks by relevance
    """
    filters = SearchFilter(
        origin=origin,
        tags=tags or [],
        limit=limit,
    )

    search_results = await search_svc.search(q, filters=filters)
    return [RouteResponse.from_orm(r.route) for r in search_results]


@router.post("/{route_id}/copy")
async def copy_route(route_id: str, db: AsyncSession = Depends(get_db)):
    """Increment route copy count."""
    route = await db.get(Route, route_id)
    if route:
        route.copy_count += 1
        await db.commit()
    return {"route_id": route_id, "copy_count": route.copy_count if route else 0}
