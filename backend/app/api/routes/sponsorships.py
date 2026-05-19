import uuid
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.api.routes.websocket import push_notification
from app.models.schemas import SponsorshipCreateRequest, SponsorshipResponse
from app.models.db import Sponsorship, TravelGoal

router = APIRouter()


@router.post("/create", response_model=SponsorshipResponse)
async def create_sponsorship(body: SponsorshipCreateRequest, db: AsyncSession = Depends(get_db)):
    sponsorship = Sponsorship(
        id=str(uuid.uuid4()),
        goal_id=body.goal_id,
        sponsor_wallet=body.sponsor_wallet,
        amount_sol=body.amount_sol,
        tx_signature=body.tx_signature,
    )
    db.add(sponsorship)
    await db.commit()
    await db.refresh(sponsorship)

    goal = await db.get(TravelGoal, body.goal_id)
    if goal:
        asyncio.create_task(
            push_notification(
                goal.user_wallet,
                {
                    "type": "sponsorship",
                    "message": f"{body.amount_sol} SOL sponsorluk alındı: {goal.origin} → {goal.destination}",
                },
            )
        )

    return sponsorship


@router.get("/{goal_id}", response_model=list[SponsorshipResponse])
async def get_sponsorships(goal_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sponsorship).where(Sponsorship.goal_id == goal_id).order_by(Sponsorship.created_at.desc()))
    sponsorships = result.scalars().all()
    if sponsorships is None:
        raise HTTPException(status_code=404, detail="Goal not found or no sponsorships")
    return sponsorships
