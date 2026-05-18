from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models.db import Route
from app.models.schemas import RouteResponse

router = APIRouter()


@router.get("/search")
async def search_routes(query: str = "", limit: int = 10, db: AsyncSession = Depends(get_db)):
    # TODO: hybrid vector + keyword search
    result = await db.execute(select(Route).limit(limit))
    return result.scalars().all()


@router.post("/{route_id}/copy")
async def copy_route(route_id: str, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if route:
        route.copy_count += 1
        await db.commit()
    return {"route_id": route_id, "copy_count": route.copy_count if route else 0}
