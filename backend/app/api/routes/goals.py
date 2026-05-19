import json
import uuid
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.db import PriceHistory, TravelGoal
from app.models.schemas import GoalCreateRequest, GoalResponse
from app.services.amadeus_client import search_flights, search_hotels
from app.agents.orchestrator import run_goal_pipeline

router = APIRouter()
PENDING_GOALS: dict[str, GoalCreateRequest] = {}


@router.post("/create")
async def create_goal(body: GoalCreateRequest, db: AsyncSession = Depends(get_db)):
    goal_id = str(uuid.uuid4())
    goal = TravelGoal(
        id=goal_id,
        user_wallet=body.user_wallet,
        destination=body.destination,
        origin=body.origin,
        travel_date=body.travel_date,
        budget_usd=body.budget_usd,
        status="processing",
    )
    db.add(goal)
    await db.commit()

    PENDING_GOALS[goal_id] = body
    await _save_initial_price_history(goal_id, body.origin, body.destination, body.travel_date, db)
    return {"goal_id": goal_id}


async def _save_initial_price_history(goal_id: str, origin: str, destination: str, travel_date: str, db: AsyncSession) -> None:
    flights = await search_flights(origin, destination, travel_date)
    hotels = await search_hotels(destination, travel_date)
    flight_price = float(flights[0].get("price", 0)) if flights else 0.0
    hotel_price = float(hotels[0].get("price", 0)) if hotels else 0.0

    history = PriceHistory(
        goal_id=goal_id,
        flight_price_usd=flight_price,
        hotel_price_usd=hotel_price,
        is_buy_signal=False,
    )
    db.add(history)
    await db.commit()


async def _stream_goal_pipeline(goal_id: str, body: GoalCreateRequest, db: AsyncSession) -> AsyncGenerator[str, None]:
    final_report: str | None = None

    async for event in run_goal_pipeline(goal_id, body):
        yield event
        if event.startswith("event: done"):
            try:
                payload = json.loads(event.split("data: ", 1)[1])
                final_report = payload.get("report")
            except Exception:
                pass

    if final_report:
        goal = await db.get(TravelGoal, goal_id)
        if goal:
            goal.final_report_md = final_report
            goal.status = "complete"
            await db.commit()

    PENDING_GOALS.pop(goal_id, None)


@router.get("/stream/{goal_id}")
async def stream_goal(goal_id: str, db: AsyncSession = Depends(get_db)):
    body = PENDING_GOALS.get(goal_id)
    if not body:
        raise HTTPException(status_code=404, detail="Goal not ready for stream")

    return StreamingResponse(_stream_goal_pipeline(goal_id, body, db), media_type="text/event-stream")


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: str, db: AsyncSession = Depends(get_db)):
    goal = await db.get(TravelGoal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.get("/list")
async def list_goals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TravelGoal).order_by(TravelGoal.created_at.desc()).limit(50))
    return result.scalars().all()


@router.get("/list/by-wallet")
async def list_goals_by_wallet(user_wallet: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TravelGoal).where(TravelGoal.user_wallet == user_wallet).order_by(TravelGoal.created_at.desc()))
    return result.scalars().all()


@router.get("/{goal_id}/price-history")
async def get_price_history(goal_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PriceHistory).where(PriceHistory.goal_id == goal_id).order_by(PriceHistory.recorded_at.asc())
    )
    return result.scalars().all()
