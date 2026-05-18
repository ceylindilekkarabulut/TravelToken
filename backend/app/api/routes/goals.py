import uuid
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.schemas import GoalCreateRequest, GoalResponse
from app.models.db import TravelGoal
from app.agents.orchestrator import run_goal_pipeline

router = APIRouter()


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

    return StreamingResponse(
        run_goal_pipeline(goal_id, body, db),
        media_type="text/event-stream",
    )


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: str, db: AsyncSession = Depends(get_db)):
    goal = await db.get(TravelGoal, goal_id)
    return goal


@router.get("/list/by-wallet")
async def list_goals(user_wallet: str, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(
        select(TravelGoal).where(TravelGoal.user_wallet == user_wallet)
    )
    return result.scalars().all()
