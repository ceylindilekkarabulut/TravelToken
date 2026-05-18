from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.db import TravelGoal
from app.services.solana_service import release_funds
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/approve-purchase")
async def approve_purchase(
    goal_id: str, approved: bool = True, db: AsyncSession = Depends(get_db)
):
    try:
        goal = await db.get(TravelGoal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        if approved:
            if not goal.solana_goal_pda:
                raise HTTPException(
                    status_code=400, detail="Goal has no Solana PDA initialized"
                )

            tx_signature = await release_funds(goal.solana_goal_pda, goal.user_wallet)

            goal.status = "completed"
            db.add(goal)
            await db.commit()

            logger.info(
                "goal_approved_and_released",
                goal_id=goal_id,
                tx_signature=tx_signature,
            )

            return {
                "status": "released",
                "goal_id": goal_id,
                "tx_signature": tx_signature,
            }
        else:
            goal.status = "rejected"
            db.add(goal)
            await db.commit()

            logger.info("goal_rejected", goal_id=goal_id)

            return {"status": "rejected", "goal_id": goal_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("approve_purchase_error", goal_id=goal_id, error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
