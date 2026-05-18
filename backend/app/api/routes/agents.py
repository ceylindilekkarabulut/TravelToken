from fastapi import APIRouter

router = APIRouter()


@router.post("/approve-purchase")
async def approve_purchase(goal_id: str, approved: bool):
    # TODO: trigger Solana release_funds if approved
    return {"goal_id": goal_id, "approved": approved}
