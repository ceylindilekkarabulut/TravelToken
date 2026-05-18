from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, case
from sqlalchemy.orm import Session as SQLSession

from app.api.deps import get_db
from app.models.db import Route
from app.models.schemas import RouteResponse
from app.services.embedding_service import embed_text
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/search")
async def search_routes(query: str = "", limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        if not query:
            result = await db.execute(select(Route).limit(limit))
            return result.scalars().all()

        query_lower = query.lower()

        embedding = await embed_text(query)

        keyword_match = case(
            (Route.origin.ilike(f"%{query}%"), 1.0),
            (Route.destination.ilike(f"%{query}%"), 1.0),
            (Route.tags.ilike(f"%{query}%"), 0.8),
            (Route.description_md.ilike(f"%{query}%"), 0.6),
            else_=0.0,
        )

        stmt = select(
            Route,
            keyword_match.label("keyword_score"),
            (1.0 - (Route.embedding.op("<->")(embedding))).label("vector_score")
        ).where(
            or_(
                Route.origin.ilike(f"%{query}%"),
                Route.destination.ilike(f"%{query}%"),
                Route.tags.ilike(f"%{query}%"),
                Route.description_md.ilike(f"%{query}%"),
                Route.embedding.is_not(None)
            )
        ).order_by(
            (0.6 * (1.0 - (Route.embedding.op("<->")(embedding))) + 0.4 * keyword_match).desc()
        ).limit(limit)

        result = await db.execute(stmt)
        rows = result.all()
        return [row[0] for row in rows]
    except Exception as e:
        logger.error("search_routes_error", error=str(e))
        result = await db.execute(select(Route).limit(limit))
        return result.scalars().all()


@router.post("/{route_id}/copy")
async def copy_route(route_id: str, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, route_id)
    if route:
        route.copy_count += 1
        await db.commit()
    return {"route_id": route_id, "copy_count": route.copy_count if route else 0}
