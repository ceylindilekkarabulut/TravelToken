import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.api.routes.websocket import push_notification
from app.models.db import TravelGoal
from app.services.solana_service import release_funds

router = APIRouter()


@router.post("/approve-purchase")
async def approve_purchase(goal_id: str, approved: bool, db: AsyncSession = Depends(get_db)):
    goal = await db.get(TravelGoal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    if approved:
        if not goal.solana_goal_pda:
            raise HTTPException(status_code=400, detail="Goal has no Solana PDA")
        tx_signature = await release_funds(goal_id, goal.user_wallet)
        goal.status = "released"
        await db.commit()
        asyncio.create_task(
            push_notification(
                goal.user_wallet,
                {
                    "type": "release",
                    "message": f"Funds released for goal {goal_id}. Tx: {tx_signature}",
                },
            )
        )
        return {"goal_id": goal_id, "approved": True, "tx_signature": tx_signature}

    goal.status = "purchase_rejected"
    await db.commit()
    asyncio.create_task(
        push_notification(
            goal.user_wallet,
            {
                "type": "purchase_rejected",
                "message": f"Purchase approval rejected for goal {goal_id}.",
            },
        )
    )
    return {"goal_id": goal_id, "approved": False}
